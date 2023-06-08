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
        {'f': 'N_S (F,id=1,  birth_day=1,)\nNAME SURNAME (F,   id=2,  birth_day=1,)'},
        # spaces allowed after ), because it  is rstrip() 
        {'f': 
        'm(M,id=1,birth_day=1954,) \nf(F,id=2,birth_day=1,death_day=9,maiden_name=m,)'},
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
def test_is_id_duplicated(tmp_files):
    with pytest.raises(DuplicatedPersonIDError) as e:    #DuplicatedPersonIDError
        t.Family(tmp_files / 'f')
        
    part_of_expected_error_text = \
    'Person from line=2, have same id(already defined) as person from line=1--->Person'
    assert str(e.value).startswith(part_of_expected_error_text)

# missing second person in household
@pytest.mark.parametrize('tmp_files', [
        {'f': 'a(M, id=1, birth_day=1,)'},
    ],
    indirect=['tmp_files'],
)
def test_is_household_completed(tmp_files):
    with pytest.raises(ValueError) as e:    #DuplicatedPersonIDError
        t.Family(tmp_files / 'f')
        
    start_with_error_text = 'Household '
    ends_with_error_text = '), person2=None), not completed, missing second person.'
    assert str(e.value).startswith(start_with_error_text)
    assert str(e.value).endswith(ends_with_error_text)