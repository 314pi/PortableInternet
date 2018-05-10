
********************************************************************
 How PopMan translation files work:
********************************************************************

Everytime when PopMan translates some sort of text, the program
tries to find the wanted English text in the first row of the 
current language file. If the text is found, the row after is
used. If it is not found, the default English text will be used
instead. Therefore you can create partial translations or
change the default English text, for example "From" could become
"Sender" etc.
 
The lookup is case sensitive and only the first occurence of a
phrase is considered.


********************************************************************
 How to create a translation file for your language:
********************************************************************

Just take the "Translation.lng" file in PopMan's "Languages" directory,
rename it to your language name (the English name!) and translate all
strings in this file.

If you're done translating and want to share it, just mail it to me
and I'll be grateful to publish it on the PopMan Website.

To make the file a valid translation file it must contain the
following lines:

Language=English name of language
Author=Author's name
Email=Author's email address
Date=Date of last modification using this format: mm/dd/yyyy example: 08/28/2003
Comment=Comment in English, like: "PopMan 1.2 German Translation"
LangID=Language Identifier (see table below)


Language	LangID

Afrikaans	54
Albanian	28
Arabic		01
Armenian	43
Assamese	77
Azeri		44
Basque		45
Belarusian	35
Bengali		69
Bulgarian	02
Catalan		03
Chinese		04
Croatian	26
Czech		05
Danish		06
Dutch		19
English		09
Estonian	37
Faeroese	56
Farsi		41
Finnish		11
French		12
Georgian	55
German		07
Greek		08
Gujarati	71
Hebrew		13
Hindi		57
Hungarian	14
Icelandic	15
Indonesian	33
Italian		16
Japanese	17
Kannada		75
Kashmiri	96
Kazak		63
Konkani		87
Korean		18
Latvian		38
Lithuanian	39
Macedonian	47
Malay		62
Malayalam	76
Manipuri	88
Marathi		78
Nepali		97
Norwegian	20
Oriya		72
Polish		21
Portuguese	22
Punjabi		70
Romanian	24
Russian		25
Sanskrit	79
Serbian		26
Sindhi		89
Slovak		27
Slovenian	36
Spanish		10
Swahili		65
Swedish		29
Tamil		73
Tatar		68
Telugu		74
Thai		30
Turkish		31
Ukrainian	34
Urdu		32
Uzbek		67
Vietnamese	42

