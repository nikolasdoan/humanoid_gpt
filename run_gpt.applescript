tell application "System Events"
    repeat
        set keyDown to (key code of (key down))
        if keyDown is 16 then
            -- Play key pressed, run gpt.py script
            do shell script "python /Users/mac/Desktop/dustin/GPTAPI/gpt.py"
        end if
        delay 0.1
    end repeat
end tell
