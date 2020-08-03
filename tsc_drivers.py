import ee, gee
import argparse
import re
gee.init()

#
# DATA
#
PROJECT_ROOT='projects/wri-datalab/TSC_DRIVERS/2019'
TSC_DRIVERS_ID=PROJECT_ROOT+'/lossyear_classification'
HANSEN_THRESHOLDED_LOSS_ID='projects/wri-datalab/umd/HANSEN_BINARY_LOSS_19'


#
# IMAGES
#
HANSEN_THRESHOLDED_LOSS=ee.Image(HANSEN_THRESHOLDED_LOSS_ID)
TSC_DRIVERS=ee.Image(TSC_DRIVERS_ID)


#
# CONFIG
#
CRS="EPSG:4326"
SCALE=27.829872698318393
Z_LEVELS=[156000,78000,39000,20000,10000,4900,2400,1200,611,305,152,76,38,19]
MAX_PIXS=65500
FULL_INTENSITY=255
BANDS=['intensity','class','lossyear']
# GCE_TILE_ROOT='v2020'
THRESHOLDS=[10,15,20,25,30,50,75]
DEFAULT_GEOM_NAME='hansen_world'
DEFAULT_VERSION=2
TEST_RUN=False
NOISY=True
Z_MAX=12




#
# GEOMETRY
#
geom=None
geom_name=None
#geoms_ft=ee.FeatureCollection('ft:13BvM9v1Rzr90Ykf1bzPgbYvbb8kGSvwyqyDwO8NI')
def get_geom():
    return ee.Geometry.MultiPolygon([[[[180.0, -50.0], [180.0, -60.0], [170.0, -60.0], [160.0, -60.0], [150.0, -60.0],
                                       [150.0, -50.0], [140.0, -50.0], [140.0, -40.0], [130.0, -40.0], [120.0, -40.0],
                                       [110.0, -40.0], [110.0, -30.0], [110.0, -20.0], [100.0, -20.0], [90.0, -20.0],
                                       [90.0, -10.0], [90.0, 0.0], [80.0, 0.0], [80.0, -10.0], [70.0, -10.0],
                                       [70.0, -20.0], [60.0, -20.0], [60.0, -30.0], [50.0, -30.0], [40.0, -30.0],
                                       [40.0, -40.0], [30.0, -40.0], [20.0, -40.0], [10.0, -40.0], [10.0, -30.0],
                                       [10.0, -20.0], [10.0, -10.0], [0.0, -10.0], [0.0, 0.0], [-10.0, 0.0],
                                       [-10.0, -10.0], [-20.0, -10.0], [-20.0, 0.0], [-20.0, 10.0], [-30.0, 10.0],
                                       [-30.0, 20.0], [-20.0, 20.0], [-20.0, 30.0], [-30.0, 30.0], [-40.0, 30.0],
                                       [-40.0, 40.0], [-30.0, 40.0], [-20.0, 40.0], [-10.0, 40.0], [-10.0, 50.0],
                                       [-20.0, 50.0], [-20.0, 60.0], [-30.0, 60.0], [-40.0, 60.0], [-40.0, 50.0],
                                       [-50.0, 50.0], [-50.0, 40.0], [-60.0, 40.0], [-60.0, 30.0], [-70.0, 30.0],
                                       [-70.0, 20.0], [-60.0, 20.0], [-50.0, 20.0], [-50.0, 10.0], [-40.0, 10.0],
                                       [-40.0, 0.0], [-30.0, 0.0], [-30.0, -10.0], [-30.0, -20.0], [-40.0, -20.0],
                                       [-40.0, -30.0], [-50.0, -30.0], [-50.0, -40.0], [-60.0, -40.0], [-60.0, -50.0],
                                       [-50.0, -50.0], [-40.0, -50.0], [-30.0, -50.0], [-20.0, -50.0], [-20.0, -60.0],
                                       [-30.0, -60.0], [-40.0, -60.0], [-50.0, -60.0], [-60.0, -60.0], [-70.0, -60.0],
                                       [-80.0, -60.0], [-80.0, -50.0], [-80.0, -40.0], [-90.0, -40.0], [-90.0, -30.0],
                                       [-90.0, -20.0], [-80.0, -20.0], [-80.0, -10.0], [-90.0, -10.0], [-100.0, -10.0],
                                       [-100.0, 0.0], [-100.0, 10.0], [-110.0, 10.0], [-120.0, 10.0], [-120.0, 20.0],
                                       [-120.0, 30.0], [-130.0, 30.0], [-130.0, 40.0], [-130.0, 50.0], [-140.0, 50.0],
                                       [-150.0, 50.0], [-160.0, 50.0], [-170.0, 50.0], [-180.0, 50.0], [-180.0, 60.0],
                                       [-180.0, 70.0], [-180.0, 80.0], [-170.0, 80.0], [-160.0, 80.0], [-150.0, 80.0],
                                       [-140.0, 80.0], [-130.0, 80.0], [-120.0, 80.0], [-110.0, 80.0], [-100.0, 80.0],
                                       [-90.0, 80.0], [-80.0, 80.0], [-70.0, 80.0], [-60.0, 80.0], [-50.0, 80.0],
                                       [-40.0, 80.0], [-30.0, 80.0], [-20.0, 80.0], [-10.0, 80.0], [0.0, 80.0],
                                       [0.0, 70.0], [10.0, 70.0], [10.0, 80.0], [20.0, 80.0], [30.0, 80.0],
                                       [40.0, 80.0], [50.0, 80.0], [60.0, 80.0], [70.0, 80.0], [80.0, 80.0],
                                       [90.0, 80.0], [100.0, 80.0], [110.0, 80.0], [120.0, 80.0], [130.0, 80.0],
                                       [140.0, 80.0], [150.0, 80.0], [160.0, 80.0], [170.0, 80.0], [180.0, 80.0],
                                       [180.0, 70.0], [180.0, 60.0], [180.0, 50.0], [170.0, 50.0], [160.0, 50.0],
                                       [160.0, 40.0], [150.0, 40.0], [150.0, 30.0], [160.0, 30.0], [160.0, 20.0],
                                       [170.0, 20.0], [180.0, 20.0], [180.0, 10.0], [180.0, 0.0], [180.0, -10.0],
                                       [180.0, -20.0], [180.0, -30.0], [180.0, -40.0], [180.0, -50.0]],
                                      [[150.0, -50.0], [160.0, -50.0], [160.0, -40.0], [150.0, -40.0], [150.0, -50.0]],
                                      [[160.0, -40.0], [170.0, -40.0], [170.0, -30.0], [160.0, -30.0], [160.0, -40.0]],
                                      [[70.0, -10.0], [70.0, 0.0], [70.0, 10.0], [70.0, 20.0], [60.0, 20.0],
                                       [60.0, 10.0], [60.0, 0.0], [60.0, -10.0], [70.0, -10.0]],
                                      [[160.0, 20.0], [150.0, 20.0], [150.0, 10.0], [160.0, 10.0], [160.0, 20.0]]],
                                     [[[0.0, -50.0], [10.0, -50.0], [10.0, -60.0], [0.0, -60.0], [0.0, -50.0]]], [
                                         [[80.0, -40.0], [80.0, -50.0], [80.0, -60.0], [70.0, -60.0], [60.0, -60.0],
                                          [60.0, -50.0], [50.0, -50.0], [50.0, -40.0], [60.0, -40.0], [70.0, -40.0],
                                          [70.0, -30.0], [80.0, -30.0], [80.0, -40.0]]], [
                                         [[-10.0, -40.0], [0.0, -40.0], [0.0, -50.0], [-10.0, -50.0], [-20.0, -50.0],
                                          [-20.0, -40.0], [-20.0, -30.0], [-10.0, -30.0], [-10.0, -40.0]]], [
                                         [[-110.0, -20.0], [-100.0, -20.0], [-100.0, -30.0], [-110.0, -30.0],
                                          [-110.0, -20.0]]],
                                     [[[-30.0, -20.0], [-20.0, -20.0], [-20.0, -30.0], [-30.0, -30.0], [-30.0, -20.0]]],
                                     [[[-10.0, -10.0], [0.0, -10.0], [0.0, -20.0], [-10.0, -20.0], [-10.0, -10.0]]], [
                                         [[-170.0, -40.0], [-170.0, -50.0], [-180.0, -50.0], [-180.0, -40.0],
                                          [-180.0, -30.0], [-180.0, -20.0], [-180.0, -10.0], [-180.0, 0.0],
                                          [-180.0, 10.0], [-170.0, 10.0], [-170.0, 20.0], [-180.0, 20.0],
                                          [-180.0, 30.0], [-170.0, 30.0], [-160.0, 30.0], [-150.0, 30.0],
                                          [-150.0, 20.0], [-150.0, 10.0], [-150.0, 0.0], [-140.0, 0.0], [-130.0, 0.0],
                                          [-130.0, -10.0], [-130.0, -20.0], [-120.0, -20.0], [-120.0, -30.0],
                                          [-130.0, -30.0], [-140.0, -30.0], [-150.0, -30.0], [-160.0, -30.0],
                                          [-160.0, -20.0], [-170.0, -20.0], [-170.0, -30.0], [-170.0, -40.0]]]], None,
                                    False)


#
# Methods:
#
def zintensity(img,z,scale=SCALE):
    reducer=ee.Reducer.mean()
    return reduce(img,z,scale,reducer)


def zmode(img,z,scale=SCALE):
    img=img.updateMask(img.gt(0))
    reducer=ee.Reducer.mode()
    return reduce(img,z,scale,reducer)


def reduce(img,z,scale,reducer):
    if (z==Z_MAX): 
        return img
    else:
        return img.reproject(
                    scale=scale,
                    crs=CRS
            ).reduceResolution(
                    reducer=reducer,
                    maxPixels=MAX_PIXS
            ).reproject(
                    scale=Z_LEVELS[z],
                    crs=CRS
            )


def zjoin(img_i,img_cat,img_ly):
    return img_i.addBands([img_cat,img_ly]).toInt().rename(BANDS)


#
# EXPORTERS
#
def export_tiles(image,z,v,threshold):
    tiles_path=gce_tiles_path(v,threshold)
    name=tiles_path.replace('/','__')
    print('tiles:',z,tiles_path,name)
    image=image.unmask(0).updateMask(1)
    if not TEST_RUN:
        task=ee.batch.Export.map.toCloudStorage(
            fileFormat='png',
            image=image,
            description='{}__{}'.format(name,z), 
            bucket='tsc_tree_cover_loss_drivers',
            path=tiles_path, 
            writePublicTiles=False, 
            maxZoom=z, 
            minZoom=z, 
            region=geom.bounds(),
            skipEmptyTiles=True
        )
        task.start()
        if NOISY: print(task.status())
        return task


def export_asset(image,z,v,threshold):
    name=zlevel_asset_name(v,z,threshold)
    print('asset:',z,name)
    if not TEST_RUN:
        task=ee.batch.Export.image.toAsset(
            image=image, 
            description=name, 
            assetId='{}/{}'.format(PROJECT_ROOT,name), 
            scale=Z_LEVELS[z], 
            crs=CRS, 
            region=geom.bounds(),
            maxPixels=500000000
        )
        task.start()
        if NOISY: print(task.status())
        return task


#
# RUN
#
def run(img_i,img_cat,img_ly,maxz,minz,v,threshold,scale=SCALE,lowest_to_asset='False'):
    for z in range(minz,maxz+1):
        zimg_i=zintensity(img_i,z,scale)
        zimg_cat=zmode(img_cat,z,scale)
        zimg_ly=zmode(img_ly,z,scale)
        zimg=zjoin(zimg_i,zimg_cat,zimg_ly)
        if z==minz:
            if (not lowest_to_asset) or (isinstance(lowest_to_asset,str) and lowest_to_asset.lower()=='false'):
                print('skiping inside-asset-export')
            else:
                print('export asset:',z)
                task=export_asset(zimg,z,v,threshold)
        task=export_tiles(zimg,z,v,threshold)


def run_zasset(img_i,img_cat,img_ly,z,v,threshold,scale=SCALE):
    zimg_i=zintensity(img_i,z,scale)
    zimg_cat=zmode(img_cat,z,scale)
    zimg_ly=zmode(img_ly,z,scale)
    zimg=zjoin(zimg_i,zimg_cat,zimg_ly)
    print('export asset:',z)
    task=export_tiles(zimg,z,v,threshold)


#
# PATH/IMG/IC HELPERS
#
def gce_tiles_path(v,threshold):
    return 'v{}/tcd_{}'.format(v,threshold)


def zlevel_asset_name(v,z,threshold):
    gname=re.sub('^hansen','',geom_name)
    gname=re.sub('^_','',gname)
    return re.sub('\.','-','tsc_drivers_{}_v{}_z{}_tc{}'.format(gname,v,z,threshold))


def zlevel_asset(v,z,threshold):
    return ee.Image('{}/{}'.format(PROJECT_ROOT,zlevel_asset_name(v,z,threshold)))


#
# MAIN
#
def _inside(args):
    img_i=HANSEN_THRESHOLDED_LOSS.select(['loss_{}'.format(args.threshold)])
    img_cat=TSC_DRIVERS.select(['class'])
    img_ly=TSC_DRIVERS.select(['lossyear'])
    run(img_i,img_cat,img_ly,int(args.max),int(args.min),args.version,args.threshold,lowest_to_asset=args.asset)


def _outside(args):
    last_z=int(args.max)+1
    scale=Z_LEVELS[last_z]
    img=zlevel_asset(args.version,last_z,args.threshold)
    img_i=img.select(['intensity'])
    img_cat=img.select(['class'])
    img_ly=img.select(['lossyear'])
    run(img_i,img_cat,img_ly,int(args.max),int(args.min),args.version,args.threshold,scale,False)


def _zasset(args):
    img_i=HANSEN_THRESHOLDED_LOSS.select(['loss_{}'.format(args.threshold)])
    img_cat=TSC_DRIVERS.select(['class'])
    img_ly=TSC_DRIVERS.select(['lossyear'])
    run_zasset(img_i,img_cat,img_ly,int(args.z_level),args.version,args.threshold)


def main():
    global geom_name, geom
    parser=argparse.ArgumentParser(description='TSC Drivers')
    parser.add_argument('-g','--geom_name',default=DEFAULT_GEOM_NAME,help='geometry name (https://fusiontables.google.com/DataSource?docid=13BvM9v1Rzr90Ykf1bzPgbYvbb8kGSvwyqyDwO8NI)')
    parser.add_argument('-v','--version',default=DEFAULT_VERSION,help='version')
    parser.add_argument('threshold',help='treecover 2000:\none of {}'.format(THRESHOLDS))
    subparsers=parser.add_subparsers()
    parser_inside=subparsers.add_parser('inside', help='export the zoomed in z-levels')
    parser_inside.add_argument('-max','--max',default=12,help='max level')
    parser_inside.add_argument('-min','--min',default=7,help='min level')
    parser_inside.add_argument('-a','--asset',default='True',help='export min level to asset')
    parser_inside.set_defaults(func=_inside)
    parser_outside=subparsers.add_parser('outside', help='export the zoomed out z-levels')
    parser_outside.add_argument('-max','--max',default=6,help='max level')
    parser_outside.add_argument('-min','--min',default=2,help='min level')
    parser_outside.set_defaults(func=_outside)
    parser_zasset=subparsers.add_parser('zasset', help='export z-level to asset')
    parser_zasset.add_argument('-z','--z_level',default=7,help='max level')
    parser_zasset.set_defaults(func=_zasset)
    args=parser.parse_args()
    if int(args.threshold) in THRESHOLDS: 
        geom_name=args.geom_name
        geom=get_geom()
        args.func(args)
    else: 
        print('INVALID THRESHOLD:',args.threshold,args)


if __name__ == "__main__":
    main()
