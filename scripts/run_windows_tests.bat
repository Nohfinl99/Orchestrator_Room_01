@echo off
REM Corrected Windows launcher for the control-room slice, runner v2.
REM Code root and tooling root are SEPARATE. This BAT never cd's into
REM the tooling checkout to test a different tree, and it never prints
REM "Done" on failure: the helper exit code is propagated exactly.
REM
REM Usage (from any working directory):
REM   <tooling>\scripts\run_windows_tests.bat <code-root> <pinned-manifest> [output-base]
REM   <code-root>       = detached code worktree at the target commit
REM   <pinned-manifest> = JSON with code_commit, pin_origin, source_digests
REM   [output-base]     = directory OUTSIDE code and tooling roots
REM                       (default: %CD%\windows-runs)
REM Exit codes: 0 pass, 1 test failure, 2 preflight failure,
REM             3 collection/source-change failure, plus py launcher errors.
setlocal
if "%~1"=="" (
  echo Usage: run_windows_tests.bat ^<code-root^> ^<pinned-manifest^> [output-base]
  exit /b 2
)
if "%~2"=="" (
  echo Usage: run_windows_tests.bat ^<code-root^> ^<pinned-manifest^> [output-base]
  exit /b 2
)
set "CODE_ROOT=%~1"
set "PINNED=%~2"
if "%~3"=="" (
  set "OUTPUT_BASE=%CD%\windows-runs"
) else (
  set "OUTPUT_BASE=%~3"
)
set "TOOLING_ROOT=%~dp0.."
py -3.14 -X utf8 "%TOOLING_ROOT%\scripts\run_windows_tests.py" --source-root "%CODE_ROOT%" --pinned-manifest "%PINNED%" --output-base "%OUTPUT_BASE%" --mode git
set "HELPER_EXIT=%ERRORLEVEL%"
if %HELPER_EXIT% NEQ 0 (
  echo [runner] helper failed with exit %HELPER_EXIT%; NOT a successful run.
  exit /b %HELPER_EXIT%
)
echo Done. Helper exit 0. Send the unique run directory (test-run.log + manifest.json) back to Muse in direct chat.
exit /b 0
endlocal
