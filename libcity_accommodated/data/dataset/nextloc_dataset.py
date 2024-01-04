import torch
from libcity.data.dataset import BaseDataset, padding_mask


class NextLocDataset(BaseDataset):
    def __init__(self, config):
        super().__init__(config)
        self.collate_fn = collate_superv_nextloc


def collate_superv_nextloc(data, max_len=None, vocab=None, add_cls=True):
    batch_size = len(data)
    features, temporal_mat = zip(*data)  # list of (seq_length, feat_dim)

    # Stack and pad features and masks (convert 2D to 3D tensors, i.e. add batch dimension)
    lengths = [X.shape[0] for X in features]  # original sequence length for each time series
    if max_len is None:
        max_len = max(lengths)
    X = torch.zeros(batch_size, max_len, features[0].shape[-1],
                    dtype=torch.long)  # (batch_size, padded_length, feat_dim)
    batch_temporal_mat = torch.zeros(batch_size, max_len, max_len,
                                     dtype=torch.long)  # (batch_size, padded_length, padded_length)

    labels = []
    update_length = []
    for i in range(batch_size):
        if lengths[i] <= max_len:
            end = lengths[i] - 1
        else:
            end = max_len - 1

        update_length.append(end)
        # labels.append(float((features[i][end][1] - start_time) / 60))
        labels.append((features[i][end][0]))

        X[i, :end, :] = features[i][:end, :]
        if add_cls:
            X[i, 2:end, 2:4] = vocab.pad_index
        else:
            X[i, 1:end, 2:4] = vocab.pad_index

        X[i][end][0] = X[i][end - 1][0]

    targets = torch.LongTensor(labels).unsqueeze(-1)  # (batch_size, 1)

    padding_masks = padding_mask(torch.tensor(update_length, dtype=torch.int16), max_len=max_len)

    return X.long(), targets.long(), padding_masks, batch_temporal_mat.long()  # batch_temporal_mat全0
