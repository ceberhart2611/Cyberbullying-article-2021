USE [bullyingdb]
GO


SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[LR_allfeatures](
	[commentid] [nvarchar](max) NOT NULL,
	[doc_positive_confidence] [nvarchar](max) NOT NULL,
	[doc_neutral_confidence] [nvarchar](max) NOT NULL,
	[doc_negative_confidence] [nvarchar](max) NOT NULL,
	[linkpresence] [int] NOT NULL,
	[doccursing] [nvarchar](max) NULL,
	[doccontext] [nvarchar](max) NULL,
	[docgeneral] [nvarchar](max) NULL,
	[docsexlang] [nvarchar](max) NULL,
	[kpcursing] [nvarchar](max) NULL,
	[kpcontext] [nvarchar](max) NULL,
	[kpgeneral] [nvarchar](max) NULL,
	[kpsexlang] [nvarchar](max) NULL,
	[comment] [nvarchar](max) NOT NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO


