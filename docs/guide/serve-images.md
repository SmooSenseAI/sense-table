# Serving images/videos

When you work with multi-modal AI data, it is very important to view images efficiently.
SenseTable is designed to help you with that.

## Links in data file
It is often unnecessary to store images/videos content inside the data file. 
You can simply save urls in the table file, and store raw files elsewhere.

## Store images/videos files

### On your laptop
If you data size is small you can store them on your laptop to have quick iteration.
You can use Flask to serve the images via url like this:

```
http://localhost:8000/static/filename.jpg
```


### S3 or similar cloud storage
S3 is highly scalable and cost-effective.

The best storage solution depends on your data access pattern. We need to balance between network overhead and bandwidth:
- If you need batch access, it is better to package many small files into fewer and bigger files. This is mostly needed in training.
- For exploration and analytics, you mostly need low-latency random access. S3 is well-tested to serve billions of small files with 500 ms latency at 5000+ QPS.

Once you store images on S3, you will get a url like this

```
s3://sense-table-demo/datasets/COCO2017/images/000000000001.jpg
```

S3 buckets are private in most enterprise use cases. SenseTable has built-in API to sign url on demand, such that they can be displayed in the web browser.

