# Installation & Usage
> 1. Download from the [Releases page](https://github.com/hextrace/TS4move/releases/)
> - Mac users will want to download `ts4move-macos.zip`
> - Windows users will want to download `ts4move-windows.zip`
> 2. Unzip the file
> 3. Run the command using your system's elevated privileges.

---
## Windows
> 1. Open an [elevated command prompt](https://www.lifewire.com/how-to-open-an-elevated-command-prompt-2618088)
> 2. Navigate to where you downloaded the file
> 3. Type `.\ts4move.exe`

Example CMD commands:
```commandline
cd %USERPROFILE%\Downloads
.\ts4move.exe
```

Example PowerShell commands:
```commandline
cd ~\Downloads
.\ts4move.exe
```
---
## macOS
> 1. Open Terminal
> 2. Navigate to where you downloaded the file
> 3. Type `sudo ./ts4move`

Example Terminal commands:
```commandline
cd ~/Downloads/
sudo ./ts4move
```
---
# Introduction
TS4Move was born out of a frequent question I've encountered as a support member for several The Sims 4 Discord servers: *Can I move my mods and CC to another drive?*

The short answer is "**yes**".

The long answer is that it can be done by moving the TS4 folder from a user's Documents folder and then making a symbolic link (or junction) in the Documents/Electronic Arts folder to point to where you moved the files to.

This could be accomplished on Windows by running the following commands (assuming you have an external drive E:):
> 1. Open an elevated command prompt (CMD)
> 2. Type `move "%userprofile%\Documents\Electronic Arts\The Sims 4" "E:\The Sims 4"`
> 3. Wait for the command to complete
> 4. Type `mklink /j "%userprofile\Documents\Electronic Arts\The Sims 4" "E:\The Sims 4"`

In macOS, it's a similar process - let's assume you have an external drive entitled "DATA":
> 1. Open Terminal
> 2. Type `mv ~/Documents/Electronic\ Arts/The\ Sims\ 4 /Volumes/DATA/The\ Sims\ 4`
> 3. Wait for command to complete
> 4. Type `ln -s ~/Documents/Electronic\ Arts/The\ Sims\ 4 /Volumes/DATA/The\ Sims\ 4`

These two processes, however, assume that the end user is comfortable with the command-lines of their respective systems and understand how the file systems of their systems work. This utility, though crude, does the above steps for the end user with the end user only needing to select the drive that they want to move the files to.

---
# Disclaimer
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

That is to say, you are responsible for your own data. I cannot stress the importance of making backups of your important files before using ANY application that makes changes to your computer. 