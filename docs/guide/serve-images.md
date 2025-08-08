# Serving images/videos

When you work with multi-modal AI data, it is very important to view images efficiently.
SenseTable is designed to help you with that.

## Links in data file
It is often unnecessary to store images/videos content inside the data file.
You can simply save urls in the table file, and store raw files elsewhere.

## Store images/videos files

### On your laptop
If you data size is small you can store them on your laptop to have quick iteration.
You can use the built-in api to access images in your laptop. For example:

```
http://localhost:8000/api/get-file?path=~/Downloads/file-name.jpg
```


### S3 or similar cloud storage
For exploration and analytics, low-latency random access to images is often more important than high throughput.
Amazon S3 is an ideal solution — it’s scalable, cost-effective, and well-suited for storing large image datasets.

Once images are stored in S3, they are accessible via URIs like:

```
s3://sense-table-demo/datasets/COCO2017/images/000000000001.jpg
```
In most enterprise environments, S3 buckets are kept private.
To support secure access, SenseTable provides a built-in API to generate signed URLs on demand, allowing images to be safely displayed in web browsers without exposing public access.
As long as you setup AWS credentials and endpoint in the environment, it should just work out of the box.

You may also provide your custom-configured `s3_client` in the Python SDK.
