import os
import pandas as pd
import numpy as np

def process():
    input_file = os.path.expanduser('~/Work/COCO2017/organized/annotations.parquet')
    df = pd.read_parquet(input_file).reset_index(drop=True)
    df.drop(columns=['area',], inplace=True)

    print(f'Data file: {input_file}, shape: {df.shape}, columns: {df.columns}')

    df_image = pd.read_parquet(os.path.expanduser('~/Work/COCO2017/organized/images.parquet')).reset_index(drop=True)
    df_image = df_image[['image_id', 'width', 'height', 'caption']]
    df_image['caption'] = df_image['caption'].apply(lambda x: str(x[0]) if isinstance(x, (list, np.ndarray)) else None)
    df_image.rename(columns={'width': 'image_width', 'height': 'image_height', 'caption': 'image_caption'}, inplace=True)
    df = pd.merge(df, df_image, on='image_id', how='left').reset_index(drop=True)

    df['image_url'] = df['image_id'].apply(lambda x: f's3://sense-table-demo/datasets/COCO2017/images/{x:012d}.jpg') # 000000000001
    df['bbox_width'] = df['bbox'].apply(lambda x: x[2])
    df['bbox_height'] = df['bbox'].apply(lambda x: x[3])
    df['bbox_area'] = df['bbox_width'] * df['bbox_height']
    df['bbox_percentage'] = 100 * df['bbox_area'] / (df['image_width'] * df['image_height'])
    df['iscrowd'] = df['iscrowd'].astype(bool)
    df.drop(columns=[ 'index'], inplace=True)


    df.reset_index().to_parquet(input_file.replace('.parquet', '-clean.parquet'), index=False)
   
if __name__ == '__main__':
    process()