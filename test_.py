import pytest
import familytreemake_ng as t

# this is all valid one line config file, starting simple
# it must be used if you do not use it then there is error
# @pytest.mark.parametrize("input_file", [
#     "#",
#     "##",
#     "",
#     "   ",
#     "  ",
# ])

@pytest.mark.parametrize('tmp_files', [
        {'f': '#'},
        {'f': '##'},
        {'f': ''},
        {'f': '  '},
        {'f': '   '},
        {'f': '\n'},
        {'f': '\t'},
        {'f': '\t\t'},
        {'f': 'NAME_SURNAME'},      # FAIL !!!!
        {'f': 'NAME_SURNAME()'},
    ],
    indirect=['tmp_files'],
)

def test_is_input_file_valid(tmp_files):
    assert t.Family(tmp_files / 'f')



