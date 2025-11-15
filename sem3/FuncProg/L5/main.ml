type code = Elem of bool | Not | And | Or | Xor;;

exception InvalidExpression of string;;

let eval instr =
  let rec eval_rec current_instr stack =
    match (current_instr, stack) with
    | [], outcome_stack -> outcome_stack
    | (Elem b) :: rest, outcome_stack -> eval_rec rest (b :: outcome_stack)

    | Not :: rest, v :: s_rest -> eval_rec rest ((not v) :: s_rest)
    | Not :: _, [] -> raise (InvalidExpression "Brak argumentu dla Not, wymagany 1")

    | And :: rest, v1 :: v2 :: s_rest -> eval_rec rest ((v2 && v1) :: s_rest)
    | And :: _, _ -> raise (InvalidExpression "Brak argumentow dla And, wymagane 2")

    | Or :: rest, v1 :: v2 :: s_rest -> eval_rec rest ((v2 || v1) :: s_rest)
    | Or :: _, _ -> raise (InvalidExpression "Brak argumentow dla Or, wymagane 2")

    | Xor :: rest, v1 :: v2 :: s_rest -> eval_rec rest ((v2 <> v1) :: s_rest)
    | Xor :: _, _ -> raise (InvalidExpression "Brak argumentow dla Xor, wymagane 2")
  in

  let final_stack = eval_rec instr [] in

  match final_stack with
  | [result] -> result
  | _ -> raise (InvalidExpression "Niepoprawna koncowa struktura stosu")
;;


eval [Elem true; Elem false; And; Not];;

eval [Elem true; Elem true; Xor; Elem false; Or];;

eval [Elem true; Elem false; Or; Elem true; Not; And];;

eval [Elem true; Elem false; And; And];;

eval [Elem true; Not; Elem false; And];;