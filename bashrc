# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions


# added by Miniconda3 4.1.11 installer
export PATH=/home/phzd/miniconda3/bin:$PATH

## /home/admin/lib_so_for_open_use
source /home/admin/lib_so_for_open_use/add_to_bashrc
