USE [bullyingdb]
GO


SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[finalcomments30up](
	[commentid] [nvarchar](max) NOT NULL,
	[comment] [nvarchar](max) NOT NULL,
	[author] [nvarchar](max) NOT NULL,
	[subreddit] [nvarchar](max) NOT NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO


