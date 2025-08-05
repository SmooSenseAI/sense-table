# Folder Browser as a mini Catelog

Data Catelog is very useful when you want to discover and overview your data, but it is often maintained by a separate SRE team, inflexible to change and difficult to customize.

SenseTable empowers you to directly use File System as a mini catelog. Benefits:

- It is very fast to get started and flexible to make changes.
- Most of LLMs natively know how to access file systems.
- Cost effective. No need to pay for dedicated servers and databases unless it is needed.


## Folder Navigation


## Markdown description of a folder

You can optionally add `readme.md` to a folder and get it displayed when you preview the folder.



::: warning Caveats of case sensitivity
On macOS the file system is case-insensitive, so any upper/lower case of `Readme.md` or `README.MD` would work.

However S3 is case sensitive, so we need to exactly use `readmd.md` as the file name.
:::


## Preview images and videos
<ThemedVideo src="/videos/preview_images.webm" />




## Preview parquet files

Parquet files store their metadata in a dedicated footer at the end of the file. Combined with S3’s support for HTTP Range requests, this allows us to preview Parquet files by fetching only a few kilobytes — even when the full file is many gigabytes in size.

Below is an example of previewing a **100-million-row, 8.43 GB** Parquet file with minimal data transfer in only **one second**.

<ThemedVideo src="/videos/preview_parquet.webm" />

## Preview csv files

CSV is not efficient but due to it simplicity it is still widely used.
SenseTable also support efficiently previewing csv file by only fetching the first few dozen rows.

Below is an example of previewing a **856 MB** file in only **a few seconds**.

<ThemedVideo src="/videos/preview_csv.webm" />

## Preview json
We provide a built-in json viewer specially optimized for large data.
You can interactively expand/collapse and copy whole or part of the data.


<ThemedVideo src="/videos/preview_json.webm" />
