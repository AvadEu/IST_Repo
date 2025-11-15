let rec sum list = 
  let rec help (acc_a, acc_b) arr = 
    match arr with
    | [] -> [acc_a, acc_b]
    | (x, y) ::t -> 
        help (acc_a + x, acc_b + y) t
  in
  help (0, 0) list

