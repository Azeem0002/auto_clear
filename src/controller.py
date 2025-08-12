import typer
import psutil
import time
import sys
import subprocess
import os
from pathlib import Path
from typing import Union, Literal, Optional

app = typer.Typer()

PID_FILE = Path("autoclear.pid")
INTERVAL = (10 * 600) // 60


def time_format(
    seconds: Union[int, float],
    *,
    show_hours: bool = True,
    show_minutes: bool = True,
    show_seconds: bool = True,
    hour_unit: str | Literal['h'] = "h",
    minute_unit: str | Literal['m'] = "m",
    second_unit: str | Literal['s'] = "s",
    show_higher_units: bool = False,
):
    seconds = max(0, int(round(seconds)))

    hours, rem = divmod(seconds, 3600)
    mins, secs = divmod(rem, 60)

    parts = []

    if show_hours and (hours > 0):
        parts.append(f"{hours}{hour_unit}")
    if show_minutes and (mins > 0):
        parts.append(f"{mins}{minute_unit}")
    if show_seconds and (secs > 0):
        parts.append(f"{secs}{second_unit}")

    return " ".join(parts) if parts else f"0{minute_unit}"



@app.command()
def stop():
    PID_FILE = Path("autoclear.pid")

    # Combined verification approach
    try:
        pid = int(PID_FILE.read_text()) if PID_FILE.is_file() else None
    except ValueError:
        pid = None

    current_status = status(show_output=False)

    # Enhanced status check
    if not current_status["is_running"] and pid is None:
        typer.echo("autoclear is not running", err=True)
        raise typer.Exit(1)

    # Process termination with both approaches
    pids_to_stop = set()
    if pid:
        pids_to_stop.add(pid)
    if current_status["pids"]:
        pids_to_stop.update(current_status["pids"])

    stopped = False
    for pid in pids_to_stop:
        try:
            proc = psutil.Process(pid)
            proc.terminate()  # Graceful first
            try:
                proc.wait(timeout=3)
                stopped = True
            except psutil.TimeoutExpired:
                proc.kill()
                stopped = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    # Cleanup and feedback
    PID_FILE.unlink(missing_ok=True)
    if stopped:
        typer.echo(f"Stopped {len(pids_to_stop)} autoclear process(es)")
        raise typer.Exit(0)
    else:
        typer.echo("Failed to stop autoclear", err=True)
        raise typer.Exit(1)



@app.command()
def status(show_output: bool = True):
    PID_FILE = Path("autoclear.pid")
    controller_pid = os.getpid()

    pids = []
    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            if "python" not in proc.name().lower():
                continue

            cmdline = " ".join(proc.info.get("cmdline", []))

            if "autoclear" in cmdline.lower() and proc.pid != controller_pid:
                pids.append(proc.pid)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    try:
        main_pid = int(PID_FILE.read_text()) if PID_FILE.is_file() else None
        if main_pid and not psutil.pid_exists(main_pid):
            main_pid = None
    except Exception:
        main_pid = None

    result = {"is_running": bool(pids), "pids": pids, "main_pid": main_pid}

    if show_output:
        typer.echo(f"Status: {'Running' if result['is_running'] else 'Stopped'}")
        typer.echo(f"Processes: {len(result['pids']) or '0'}")
        typer.echo(f"Main PID: {result['main_pid'] or 'None'}")

    return result



@app.command()
def start(
    minutes: str = typer.Option("10", "--time", "-t", help="start using custom time"),
):
    MAX_ATTEMPTS = 2
    

    stat = status(show_output=False)
    if stat["is_running"]:
        typer.echo(
            f"autoclear already running with PID:{stat['main_pid'] or None}", err=True
        )
        raise typer.Exit(1)

    PID_FILE.unlink(missing_ok=True)

    for attempt in range(MAX_ATTEMPTS + 1):
        if minutes == "q":
            typer.echo("user quits")
            time.sleep(1)
            raise typer.Exit(1)

        try:
            min_int = int(minutes)

            if min_int > 0:
                interval = min_int * 60
                typer.echo(
                    f"autoclear starting with '{time_format(interval)}' interval"
                )
                # time.sleep(3)
                break 
            else:
                if attempt < MAX_ATTEMPTS:
                    minutes = (
                        typer.prompt(
                            f"number must be positive. {MAX_ATTEMPTS - attempt} left. try again (or q to quit)"
                        )
                        .strip()
                        .lower()
                    )

        except ValueError:
            if attempt < MAX_ATTEMPTS:
                minutes = (
                    typer.prompt(
                        f"{minutes} is not a valid number. {MAX_ATTEMPTS - attempt} left. try again (or q to quit)"
                    )
                    .strip()
                    .lower()
                )

    else:
        typer.echo(
            f"maximum attempts reached. defaulting to '{time_format(INTERVAL)}' interval"
        )
        interval = INTERVAL
        # time.sleep(3)

    autoclear_process = subprocess.Popen(
        [sys.executable, str(Path(__file__).parent / "autoclear.py"), str(interval)]
    )
    PID_FILE.write_text(str(autoclear_process.pid))
    typer.echo(f"PID: {autoclear_process.pid}")
    # time.sleep(2)



@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Auto-clear terminal controller"""
    if ctx.invoked_subcommand is None:
        start(str(INTERVAL))



if __name__ == "__main__":
    app()
