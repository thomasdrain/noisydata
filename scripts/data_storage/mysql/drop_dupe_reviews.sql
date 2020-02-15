select r.* FROM Review r
  INNER JOIN Review r2
WHERE r.Review_ScrapeID < r2.Review_ScrapeID
and r.BandID = r2.BandID
and r.AlbumID = r2.AlbumID
and r.Username = r2.Username
and r.ReviewDate = r2.ReviewDate
