######################################################################

# Here we override some settings from poky/meta/conf/bitbake.conf.  We
# do not want to modify bitbake.conf directly.

######################################################################

EXA_EXTRA_WARNINGS = ""

######################################################################

# "-Wl,--fatal-warnings" causes the linker to treat linker warnings as
# errors (kind of like -Werror).

EXA_LINK_ERRORS = ""

######################################################################

# bitbake.conf uses DEBUG_BUILD to decide whether to use
# FULL_OPTIMIZATION or DEBUG_OPTIMIZATION when setting
# SELECTED_OPTIMIZATION (which is added to CFLAGS).

# Note that optimization must be enabled in order for -Wall to catch
# some errors.

DEBUG_OPTIMIZATION = "-Og -fno-omit-frame-pointer ${DEBUG_FLAGS} -pipe"
FULL_OPTIMIZATION = "-O2 ${DEBUG_FLAGS} -pipe"

######################################################################

# Now set the desired warnings.
# In gcc -Wno-write-strings is active by default.
# In g++ -Wwrite-strings is active by default

CFLAGS   =+ "${EXA_LINK_ERRORS} -Wall ${EXA_EXTRA_WARNINGS} -Werror -rdynamic"
CXXFLAGS =+ "${EXA_LINK_ERRORS} -Wall ${EXA_EXTRA_WARNINGS} -Werror -Wno-write-strings -std=gnu++11 -rdynamic"
