#define MAX_NUM_TOKENS 2

bool succ = 0
bool canc = 0

mtype = {sync_a, cancel_a, sync_b, cancel_b};

chan cha = [0] of {mtype};
mtype pbbLog[(MAX_NUM_TOKENS * 2)];
byte pbbLogIndex = 0;

proctype alices_fsm()
{
    mtype token;

    S_init: cha?token ->
    printf("\n S_init: %e \n", token);
    pbbLog[pbbLogIndex]=token;
    pbbLogIndex++;
    if
    :: token == sync_a   -> goto S_ali_wish2exc
    :: token == cancel_a -> goto End_S_cancel
    :: token == sync_b   -> goto S_init
    :: token == cancel_b -> goto End_S_cancel
    fi

    S_ali_wish2exc: cha?token ->
    printf("\n S_ali_wish2exc: %e \n", token);
    pbbLog[pbbLogIndex]=token;
    pbbLogIndex++;
    if
    :: token == sync_a   -> goto S_ali_wish2exc
	:: token == cancel_a -> goto S_ali_wish2canc
    :: token == sync_b   -> goto End_S_success
    :: token == cancel_b -> goto End_S_cancel
    fi;

    S_ali_wish2canc: cha?token ->
    printf("\n S_ali_wish2canc: %e \n", token);
    pbbLog[pbbLogIndex]=token;
    pbbLogIndex++;
    if
    :: token == sync_a   -> goto S_ali_wish2canc
    :: token == cancel_a -> goto S_ali_wish2canc
    :: token == sync_b   -> goto End_S_success
	:: token == cancel_b -> goto End_S_cancel
    fi;

    End_S_success:
	printf("\n End_S_success: %e \n", token);
    succ = 1;
    do 
	:: token == sync_a   -> goto End_S_success
	:: token == sync_b   -> goto End_S_success
	:: token == cancel_a -> goto End_S_success
	:: token == cancel_b -> goto End_S_success
	od;

    End_S_cancel: 
	printf("\n End_S_cancel: %e \n", token);
    canc = 1;
	do
	:: token == sync_a   -> goto End_S_cancel
	:: token == sync_b   -> goto End_S_cancel
	:: token == cancel_a -> goto End_S_cancel
	:: token == cancel_b -> goto End_S_cancel
	od;
}

proctype ali()
{
    mtype token;
    byte num_tokens = 0;

    do
    :: num_tokens < MAX_NUM_TOKENS ->
        if
        :: token = sync_a
        :: token = cancel_a
        fi;
        cha!token;
        num_tokens++
    :: num_tokens >= MAX_NUM_TOKENS -> break;
    od;
}

proctype bob()
{
    mtype token;
    byte num_tokens = 0;

    do
    :: num_tokens < MAX_NUM_TOKENS ->
        if
        :: token = cancel_b
        :: token = sync_b
        fi;
        cha!token;
        num_tokens++
    :: num_tokens >= MAX_NUM_TOKENS -> break;
    od;
}

init {
    run alices_fsm();
    run ali();
    run bob();
}


never  {    /* <> (succ == 1 || canc == 1) */
T0_init:
        do
        :: atomic { ((succ == 1 || canc == 1)) -> assert(!((succ == 1 || canc == 1))) }
        :: (1) -> goto T0_init
        od;
accept_all:
        skip
}