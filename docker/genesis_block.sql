insert into blocks(
	block_id,
	version,
	previous_block_hash,
	timestamp,
	merkle_root,
	difficulty_target,
	nonce
) values (
	1,
	'1',
	'1',
	1,
	'',
	10,
	1
);

insert into  transaction_confirmations (
	transaction_confirmation_id,
	block_id,
	transaction_id
) values (
	1,
	1,
	1
);