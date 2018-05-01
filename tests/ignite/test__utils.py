import pytest
import torch
from torch.autograd import Variable
from ignite._utils import convert_tensor, to_onehot


def test_convert_tensor():
    x = torch.Tensor([0.0])
    tensor = convert_tensor(x)
    assert torch.is_tensor(tensor)

    x = (torch.Tensor([0.0]), torch.Tensor([0.0]))
    list_ = convert_tensor(x)
    assert isinstance(list_, list)
    assert torch.is_tensor(list_[0])
    assert torch.is_tensor(list_[1])

    x = {'a': torch.Tensor([0.0]), 'b': torch.Tensor([0.0])}
    dict_ = convert_tensor(x)
    assert isinstance(dict_, dict)
    assert torch.is_tensor(dict_['a'])
    assert torch.is_tensor(dict_['b'])

    assert convert_tensor('a') == 'a'

    with pytest.raises(TypeError):
        convert_tensor(12345)

    tensor = torch.Tensor([1])
    assert not tensor.requires_grad
    tensor = convert_tensor(tensor, requires_grad=True)
    assert tensor.requires_grad

    # 'convert_tensor' will not catch exceptions raised by pytorch.
    leaf = torch.Tensor([1])
    leaf.requires_grad_(True)
    not_leaf = leaf + 2
    with pytest.raises(RuntimeError):
        convert_tensor(not_leaf, requires_grad=False)


def test_to_onehot():
    indices = torch.LongTensor([0, 1, 2, 3])
    actual = to_onehot(indices, 4)
    expected = torch.eye(4)
    assert actual.equal(expected)
