type graph = (int * int list) list

let rec contains lst x =
  match lst with
  | [] -> false
  | h :: t -> h = x || contains t x

let get_neighbors g node =
  let matches = List.filter (fun (k, _) -> k = node) g in
  match matches with
  | [] -> []
  | (_, neighbors) :: _ -> neighbors

let reachable_count g start_node =
  let rec traverse visited to_visit =
    match to_visit with
    | [] -> List.length visited
    | curr :: rest ->
        if contains visited curr then
          traverse visited rest
        else
          let neighbors = get_neighbors g curr in
          traverse (curr :: visited) (List.append neighbors rest)
  in
  traverse [] [start_node]


  let g = [
  (1, [2;3]);
  (2, [4]);
  (3, [4;5]);
  (4, []);
  (5, [4])
]

(* Cykliczny *)
let g_cycle = [(1, [2]); (2, [1]); (3, [])]

let test1 = reachable_count g 1 (* 5*)
let test2 = reachable_count g_cycle 1 (* 2 *)
let test3 = reachable_count g 4 (* 4 *)
let test4 = reachable_count g 3 (* 3 *)
