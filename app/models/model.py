import random, requests

def get_random_one(entries):
    try:
        one_entry = random.choice(entries)
        word = one_entry["word"]
        return word
    except IndexError:
        return None

def get_query(params):
    response = requests.get('http://api.datamuse.com/words/', params=params)
    # The following is a result of our query.  This is a result full of rhymes
    entries = response.json()
    return entries

def generate_lines(input_word):
    rhy_in_entries = get_query({'rel_rhy': input_word})
    trg_in_entries = get_query({'rel_trg': input_word})

    rhy_in_one = get_random_one(rhy_in_entries)
    
    if rhy_in_one is None:
        line1 = "Sorry, we couldn't find a rhyming buddy for " + input_word
        line2 = ""
    else:
        trg_in_one = get_random_one(trg_in_entries)
        # This if not statement is saying if there is NOT an associated word, just print the word and the rhyming word.
        if trg_in_one is None:
            line1 = input_word
            line2 = rhy_in_one
        # This else statement is saying if there is an associated word, find the rhyme and then get its associated word.
        else:
            trg_out_entries = get_query({'rel_trg': rhy_in_one})
            trg_out_one = get_random_one(trg_out_entries)

            if trg_out_one is None:
                line1 = trg_in_one + " " + input_word
                line2 = rhy_in_one
            else:
                line1 = trg_in_one + " " + input_word
                line2 = trg_out_one + " " + rhy_in_one

    return line1, line2