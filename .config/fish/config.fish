# Don't run in command substitutions
if not status -c
    functions -c cd _base_cd

    function cd
        _base_cd $argv
        set -l cd_status $status
        echo $PWD > /tmp/fish-lastdir-$WINDOWID
        return $cd_status
    end

    # Do not run if parent window id does not exist
    if test -n "$i3wm_fish_term_parent_window_id"
        # Also do not run if parent window id does not actually have a
        # saved PWD
        if test -e /tmp/fish-lastdir-$i3wm_fish_term_parent_window_id
            cd (cat /tmp/fish-lastdir-$i3wm_fish_term_parent_window_id)
        end
    end

    # Remember initial path
    echo $PWD > /tmp/fish-lastdir-$WINDOWID
end

if type -q direnv
	eval (direnv hook fish)
end

