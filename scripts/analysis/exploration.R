source("db_connect.R")

# See: https://github.com/tidyverse/dbplyr
album = tbl(con, "vw_Album")
tally(album)
