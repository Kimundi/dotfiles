Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.Screen]::AllScreens | out-file -encoding ASCII C:\wsl\screen_geometry.txt
& "C:\Program Files\VcXsrv\vcxsrv.exe" :0 -nodecoration -wgl -clipboard -multimonitors
& ubuntu1804 -c "~/.scripts/wsl/wlaunch /mnt/c/wsl/screen_geometry.txt"
