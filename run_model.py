import argparse

from libcity.pipeline import run_model
from libcity.utils import add_other_args


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', type=str, default='trajectory_embedding', help='the name of task')
    parser.add_argument('--model', type=str, default='BERTLM', help='the name of model')
    parser.add_argument('--dataset', type=str, default='porto', help='the name of dataset')
    parser.add_argument('--config_file', type=str, default=None, help='the file name of config file')
    parser.add_argument('--exp_id', type=str, default=None, help='id of experiment')
    add_other_args(parser)
    args = parser.parse_args()


    """
    python run_model.py --model LinearETA --dataset bj --gpu_id 0 
    --config bj --pretrain_path libcity/cache/135178/model_cache/135178_BERTContrastiveLM_bj.pt
    """

    # args.model = 'LinearClassify'
    args.model = 'LinearNextLoc'
    args.dataset = 'bj'
    args.config_file = 'bj'
    args.gpu_id = 0
    args.mlm_ratio = 0.6


    # args.contra_ratio = 0.4
    # args.split = True
    # args.distribution = "geometric"
    # args.avg_mask_len = 2

    args.pretrain_path = 'libcity/cache/454824/model_cache/454824_BERTContrastiveLM_bj.pt'

    # args.model = 'LinearSim'
    # args.dataset = 'porto'
    # args.gpu_id = 0
    # args.config_file = 'porto'
    # args.query_data_path = 'porto_decup_origin_test_topk0.2_0.2_1.0_10000'
    # args.detour_data_path = 'porto_decup_detoured_test_topk0.2_0.2_1.0_10000'
    # args.origin_big_data_path = 'porto_decup_othersdetour_test_topk0.2_0.2_1.0_10000_100000'
    # args.sim_mode = 'most'
    # args.topk = [1, 5, 10]
    # args.pretrain_path = 'libcity/cache/836396/model_cache/836396_BERTContrastiveLM_porto.pt'

    dict_args = vars(args)

    other_args = {key: val for key, val in dict_args.items() if key not in [
        'task', 'model', 'dataset', 'config_file', 'saved_model', 'train'] and
        val is not None}
    run_model(task=args.task, model_name=args.model, dataset_name=args.dataset,
              config_file=args.config_file, saved_model=args.saved_model,
              train=args.train, other_args=other_args)
