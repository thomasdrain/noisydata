/****** Script for SelectTopNRows command from SSMS  ******/
SELECT count(*), max(ScrapeDate)
  FROM [metalarchives].[dbo].[DiscogLog]