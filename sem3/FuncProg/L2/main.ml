let reverse lista =
  let rec reverse_in acc l =
    match l with
    | [] -> acc
    | h :: t -> reverse_in (h :: acc) t
  in
  reverse_in [] lista
;;


let zip l1 l2 =
  let rec zip_in acc lista1 lista2 =
    match (lista1, lista2) with
    | ([], []) -> acc
    | (h1::t1, []) -> zip_in (h1 :: acc) t1 []
    | ([], h2::t2) -> zip_in (h2 :: acc) [] t2
    | (h1::t1, h2::t2) -> zip_in (h2 :: h1 :: acc) t1 t2
  in
  reverse (zip_in [] l1 l2);;


zip [1;2;3] [4;5;6];;
zip [] [1;2;3];;
zip [1;2;3] [];;
zip [] [];;