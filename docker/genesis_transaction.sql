insert into transactions(
	transaction_id,
	locktime
) values (
	1,
	0
);

insert into transaction_outputs(
	transaction_output_id,
	transaction_id,
	amount,
	locking_script,
	sender_address,
	recipient_address
) values (
  1,
  1,
  1000000000,
  'àähIö9f&E½çÖ´]¸Í1ÁàäÎtjí+åãJó:ö»o''ÞL@ÂÚrEk5
hÛë''tU£îj£])ÈÎdóá@Làâ*=a±§;q3x¤Üi<\¾t ÑÎy¥&e<\Ú÷OL%0þÌÔ ¡ud1û¨Fîu5tÞ¤`³î¯bpéÕt,1DÒ5nì4$
Úê9Ûåi	ÚLxDbµá
 äºc<×ULí!Ý©LÏÜözNH¡³hÿc9ÕõÚ²À(
þ$?=G1I³¶çÄÈ
',
  'coinbase',
  '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAznjoHvzCJtQcIYd3yj7v
gwaPlyiG6U/Qlw1G89n0bNt5anvRe+e2eKzvpy98aj6ShGu7hARE9SxAFA9bIHCB
qdAyPnrUaw7qGkeZNPHBByHe9prJSn0ZwBtfySOSbzdetO5aAwvLj5qMudW2PDz1
5mP2taGOvXqNnbcH78ZHQLvF6G+SbwuLHU5LEDSZlcy+CnvPqD67cg+QmJLneVmQ
fOBtbFHz3yDQghNrHWa+UCspUMHVGsDG6OEK7MSpPieY6TzBEYQWsikosQ+V0zBN
rSCADe3GBcJ7XzafM/gb+gzJ1eP78F1sA6Ja4ZtqInqN406PwerAXaUJa2twW652
9wIDAQAB
-----END PUBLIC KEY-----'
);
