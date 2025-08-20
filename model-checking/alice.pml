/* 
# compile the alice.pml file into C code
spin -a alice.pml

# generate the .exe file
gcc -o pan ./pan.c

# execute the model
./pan.exe -a -e -c500
*/
#define MAX_NUM_TOKENS 3

bool succ = 0
bool canc = 0

mtype = {sync_a, cancel_a, sync_b, cancel_b};
mtype = {success, canceled, in_progress}

chan channel = [0] of {mtype};
mtype pbbLog[(MAX_NUM_TOKENS * 2)];
byte pbbLogIndex = 0;

/*
Iterate through the pbb and verify its current state:
canceled: either Alice or Bob has sent a cancellation token
success: Alice and Bob have agreed on the exchange
in_progress: the exchange is ongoing, and one or neither has sent the acceptance token
*/
inline get_pbb_current_state(result) {
    byte i = 0;

    bool is_cancel_b = false;
    bool is_cancel_a = false;
    bool is_sync_a = false;
    bool is_sync_b = false;

    do
    :: (i < (MAX_NUM_TOKENS * 2)) ->
        if
        :: (pbbLog[i] == cancel_a)  -> is_cancel_a = true
        :: (pbbLog[i] == cancel_b)  -> is_cancel_b = true
        :: (pbbLog[i] == sync_a)    -> is_sync_a = true
        :: (pbbLog[i] == sync_b)    -> is_sync_b = true
        fi;

        if
        :: (is_cancel_a)            -> result = canceled; break
        :: (is_cancel_b)            -> result = canceled; break
        :: (is_sync_a && is_sync_b) -> result = success; break
        :: else                     -> in_progress
        fi;

        i++

    :: else -> break
    od;
}

/* 
Simulate Alice's FSM
*/
proctype fsm_of_alice()
{
    mtype token;
    mtype current_state;

    S_init: channel?token ->
    printf("\n S_init: %e \n", token);

    pbbLog[pbbLogIndex]=token;
    pbbLogIndex++;

    if
    :: token == sync_a   -> goto S_ali_wish2exc
    :: token == cancel_a -> goto End_S_cancel
    :: token == sync_b   -> goto S_init
    :: token == cancel_b -> goto End_S_cancel
    fi

    S_ali_wish2exc: channel?token ->
    printf("\n S_ali_wish2exc: %e \n", token);

    pbbLog[pbbLogIndex]=token;
    pbbLogIndex++;

    if
    :: token == sync_a   -> goto S_ali_wish2exc
	:: token == cancel_a -> goto S_ali_wish2canc
    :: token == sync_b || token == cancel_b ->
        get_pbb_current_state(current_state);

        if
        :: (current_state == success) -> goto End_S_success
        :: (current_state == canceled) -> goto End_S_cancel
        :: else -> skip
        fi
    fi;

    S_ali_wish2canc: channel?token ->
    printf("\n S_ali_wish2canc: %e \n", token);

    pbbLog[pbbLogIndex]=token;
    pbbLogIndex++;

    if
    :: token == sync_a   -> goto S_ali_wish2canc
    :: token == cancel_a -> goto S_ali_wish2canc
	:: token == sync_b || token == cancel_b ->
        get_pbb_current_state(current_state);

        if
        :: (current_state == success) -> goto End_S_success
        :: (current_state == canceled) -> goto End_S_cancel
        :: else -> skip
        fi
    fi;

    End_S_success:
	printf("\n End_S_success: %e \n", token);
    succ = 1;
    skip;

    End_S_cancel:
    printf("\n End_S_cancel: %e \n", token);
    canc = 1;
    skip;
}

/* 
Simulate Alice's action of sending tokens
The last token is always a retrieve token
*/
proctype alice()
{
    mtype token;
    byte num_tokens = 0;

    do
    :: num_tokens < MAX_NUM_TOKENS - 1 ->
        if
        :: token = sync_a;
        :: token = cancel_a;
        fi;

        channel!token;
        num_tokens++;
    :: else -> break;
    od;
}

/* 
Simulate Bob's action of sending tokens
The last token is always a retrieve token
*/
proctype bob()
{
    mtype token;
    byte num_tokens = 0;

    do
    :: num_tokens < MAX_NUM_TOKENS - 1 ->
        if
        :: token = sync_b;
        :: token = cancel_b;
        fi;

        channel!token;
        num_tokens++;
    :: else -> break;
    od;
}

init {
    run fsm_of_alice();
    run bob();
    run alice();
}

/* 
Verifies that neither succ nor canc are true
*/
// never {    /* [](!succ && !canc) */
//     T0_init:
//         do
//         :: (!succ || !canc) -> goto violation
//         :: else -> skip
//         od;
//     violation:
//         assert(0)
// }

/* Verifies that either succ or canc is true */
never {    /* []( !(succ || canc) ) */
    T0_init:
        do
        :: (!(succ || canc)) -> goto T0_init
        :: else -> goto violation
        od;

    violation:
        assert(0)
}
