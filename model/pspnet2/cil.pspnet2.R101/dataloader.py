import cv2
import torch
import numpy as np
from torch.utils import data

from config import config
from utils.img_utils import random_scale, random_mirror, normalize, \
    generate_random_crop_pos, random_crop_pad_to_shape, random_rotate
from matplotlib import pyplot as plt



def img_to_black(img, threshold=50):
    """Helper function to binarize greyscale images with a cut-off."""
    # img = img.astype(np.int64)
    # cv2 resize error on edge
    # quite strange
    img = img.astype(np.float)
    idx = img[:, :] > threshold
    idx_0 = img[:, :] <= threshold
    img[idx] = 1
    img[idx_0] = 0
    return img

foreground_threshold = 0.25
def patch_to_label(patch):
    df = np.mean(patch)
    if df > foreground_threshold:
        return 1
    else:
        return 0


class TrainPre(object):
    def __init__(self, img_mean, img_std):
        self.img_mean = img_mean
        self.img_std = img_std

    def __call__(self, img, gt, edge, midline):
        img, gt, edge, midline = random_rotate(img, gt, edge, midline, min_degree=-180, max_degree=180)
        img, gt, edge, midline = random_mirror(img, gt, edge, midline)
        gt = img_to_black(gt)
        edge = img_to_black(edge)
        midline = img_to_black(midline)



        if config.train_scale_array is not None:
            img, gt, scale, edge, midline = random_scale(img, gt, config.train_scale_array, edge, midline)

        

        img = normalize(img, self.img_mean, self.img_std)

        crop_size = (config.image_height, config.image_width)
        crop_pos = generate_random_crop_pos(img.shape[:2], crop_size)

        p_img, _ = random_crop_pad_to_shape(img, crop_pos, crop_size, 0)
        p_gt, _ = random_crop_pad_to_shape(gt, crop_pos, crop_size, -1)
        p_edge, _ = random_crop_pad_to_shape(edge, crop_pos, crop_size, -1)
        p_midline, _ = random_crop_pad_to_shape(midline, crop_pos, crop_size, -1)


        # fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
        # ax1.imshow(p_img)
        # ax2.imshow(p_gt)
        # ax3.imshow(p_edge)
        # ax4.imshow(p_midline)
        # plt.show()

        p_img = p_img.transpose(2, 0, 1)

        extra_dict = None

        return p_img, p_gt, p_edge, p_midline, extra_dict


def get_train_loader(engine, dataset):
    data_setting = {'img_root': config.img_root_folder,
                    'gt_root': config.gt_root_folder,
                    'train_source': config.train_source,
                    'eval_source': config.eval_source,
                    'test_source': config.test_source}
    train_preprocess = TrainPre(config.image_mean, config.image_std)

    train_dataset = dataset(data_setting, "train", train_preprocess,
                            config.niters_per_epoch * config.batch_size)

    train_sampler = None
    is_shuffle = True
    batch_size = config.batch_size

    if engine.distributed:
        train_sampler = torch.utils.data.distributed.DistributedSampler(
            train_dataset)
        batch_size = config.batch_size // engine.world_size
        is_shuffle = False

    train_loader = data.DataLoader(train_dataset,
                                   batch_size=batch_size,
                                   num_workers=config.num_workers,
                                   drop_last=False,
                                   shuffle=is_shuffle,
                                   pin_memory=True,
                                   sampler=train_sampler)

    return train_loader, train_sampler