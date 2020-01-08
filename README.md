#### TSC Drivers

Adapted from the `category_alpha` branch of [hansen_ee_preprocessing](https://github.com/wri/hansen_ee_processing/tree/category_alpha).

* The lossyears_classification asset was created with [this](https://code.earthengine.google.com/3ca1351887985f08a0f8c6ac583647f6).
* The hansen_binary_loss asset was created with [this](https://code.earthengine.google.com/983e954618d06ae9d375ce8376cf74af).

---
<a name='htiles'></a>
#### Tiles

Due to the earthengine limits discussed [here](https://groups.google.com/forum/#!topic/google-earth-engine-developers/wU4NNoWTD70) tile processing happens in 2 (and a half) steps:

1. Export Tiles for zoom-levels 12-7, and export an earthengine asset for zoom-level 7
2. Export Tiles for zoom-levels 6-2

The code can be run via the command line:

```bash
# step 1
$ python tsc_drivers.py inside

# step 2 (after the earthengine asset for zoom-level 7 has completed processing)
$ python tsc_drivers.py outside
```

There are various options like using test geometries, versioning, changing the zoom-level used as a break between step 1 and 2, and more.

```bash
python|master $ python tsc_drivers.py -h
usage: tsc_drivers.py [-h] [-g GEOM_NAME] [-v VERSION]
                       threshold {inside,outside,zasset} ...

HANSEN COMPOSITE

positional arguments:
  threshold             treecover 2000: one of [10, 15, 20, 25, 30, 50, 75]
  {inside,outside,zasset}
    inside              export the zoomed in z-levels
    outside             export the zoomed out z-levels
    zasset              export z-level to asset

optional arguments:
  -h, --help            show this help message and exit
  -g GEOM_NAME, --geom_name GEOM_NAME
                        geometry name (https://fusiontables.google.com/DataSou
                        rce?docid=13BvM9v1Rzr90Ykf1bzPgbYvbb8kGSvwyqyDwO8NI)
  -v VERSION, --version VERSION
                        version
```

---

#### NOTES

```
# copy from s3 to gcloud storage
gsutil -m cp -R s3://whrc-v4-processed gs://wri-public/tsc_drivers/2018/global
```

--- 

If there are failures:
1. get missing files
```
# bash
aws s3 ls whrc-v4-processed
gsutil ls gs://wri-public/tsc_drivers/2018/global
# python
...
aws_df[~aws_df.filename.isin(gs_df.filename)].to_csv('/Users/brook/WRI/code/TSC_Drivers/todo_files.csv',index=False)
```

2. Copy missing files
```
FILES=( 00N_010E_biomass.tif 00N_020E_biomass.tif 00N_030E_biomass.tif ... )

for f in "${FILES[@]}"
do
    echo "AWS->S3: "$f
    gsutil cp s3://whrc-v4-processed/${f} gs://wri-public/tsc_drivers/2018/global/${f}
done
```
