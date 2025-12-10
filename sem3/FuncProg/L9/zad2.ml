let rec remove_all lst target =
  match lst with
  | [] -> []
  | h :: t ->
      if h = target then remove_all t target
      else h :: remove_all t target

let rec remove_duplicates lst target =
  match lst with
  | [] -> []
  | h :: t ->
      if h = target then h :: (remove_all t target)
      else h :: (remove_duplicates t target)

let rd_test1 = remove_duplicates [1; 2; 2; 2; 3; 1; 4; 2] 2 (* [1; 2; 3; 1; 4] *)
let rd_test2 = remove_duplicates [5; 5; 5] 5                (* [5] *)
let rd_test3 = remove_duplicates [1; 2; 3] 4                (* [1; 2; 3] *)
let rd_test4 = remove_duplicates [] 1                       (* [] *)
let rd_test5 = remove_duplicates [1; 1; 2; 1] 1             (* [1; 2] *)