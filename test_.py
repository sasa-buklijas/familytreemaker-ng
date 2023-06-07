import pytest
import familytreemake_ng as t
from familytreemake_ng import ParsingError, DuplicatedPersonIDError


# correct
@pytest.mark.parametrize('tmp_files', [
        # comments start with #, can be multiple
        {'f': '#'},
        {'f': '##'},
        # empty line allowed
        {'f': ''},
        {'f': ' '},
        {'f': '  '},
        {'f': '\n'},
        {'f': '\t'},
        {'f': '\t\t'},
        {'f': '\n\t'},
        # person
        {'f': 'x(M, id=1, birth_day=1,)'},
        {'f': 'NAME_SURNAME (F,id=2,  birth_day=1,)'},
        {'f': 'NAME SURNAME (F,   id=2,  birth_day=1,)'}, 
        # spaces allowed after ), because it  is rstrip() 
        {'f': 'm(M, id=1, birth_day=1954,)        '},
        # ',' is optional in birth_day
        {'f': 'm(M,   id=1,   birth_day=1954,   )'},
        {'f': 'f(F, id=1, birth_day=1, death_day=9, maiden_name=mn,)'},

    ],
    indirect=['tmp_files'],
)
def test_is_person_line_valid(tmp_files):
    assert t.Family(tmp_files / 'f')


# error
@pytest.mark.parametrize('tmp_files', [
        {'f': ' #'}, # '#' must be first 
        {'f': 'NAME_SURNAME'},      # must have gender
        {'f': 'NAME_SURNAME(M)'},   # gender must end with ','
        {'f': 'NAME_SURNAME(M,)'},  # must have id
        {'f': 'NAME_SURNAME(M, id=1)'}, # id must end with ','
        {'f': ' NAME_SURNAME(F, id=2,)'}, # can not start with ' ' space
        {'f': 'NAME_SURNAME(F, id=3,,)'}, # only one ',' allowed everywhere
        {'f': 'm(M, id=4,)'}, # birth_day is mandatory
    ],
    indirect=['tmp_files'],
)
def test_is_person_line_invalid(tmp_files):
    with pytest.raises(ParsingError):
        t.Family(tmp_files / 'f')

# duplicated id error
@pytest.mark.parametrize('tmp_files', [
        {'f': 'a(M, id=1, birth_day=1,)\nb(F, id=1, birth_day=1,)'},
    ],
    indirect=['tmp_files'],
)
# add expected error messages
def test_is_id_duplicated(tmp_files):
    with pytest.raises(DuplicatedPersonIDError):    #DuplicatedPersonIDError
        t.Family(tmp_files / 'f')