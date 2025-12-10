let rec is_sorted lst =
  match lst with
  | [] | [_] -> true
  | h1 :: h2 :: t -> h1 <= h2 && is_sorted (h2 :: t)

let rec insert_rec lst x =
  match lst with
  | [] -> [x]
  | h :: t ->
      if x <= h then x :: h :: t
      else h :: insert_rec t x

let insert lst x =
  if is_sorted lst then insert_rec lst x
  else failwith "Lista nie jest posortowana!"

let test1 = insert [1; 3; 5; 7] 4   (* [1; 3; 4; 5; 7] *)
let test2 = insert [] 5             (* [5] *)
let test3 = insert [1; 2; 3] 0      (* [0; 1; 2; 3] *)
let test4 = insert [1; 2; 3] 5      (* [1; 2; 3; 5] *)