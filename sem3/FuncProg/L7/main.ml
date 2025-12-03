type 'a llist = LNil | LCons of 'a * (unit -> 'a llist);;

let lhd = function 
  LNil -> failwith "lhd" 
  | LCons (x, _) -> x;;

let ltl = function 
  LNil -> failwith "ltl" 
  | LCons (_, xf) -> xf();;

let rec lpodziel l =
  match l with
  | LNil -> (LNil, LNil)
  | _ -> 
      let h1 = lhd l in
      let t1 = ltl l in

      match t1 with
      | LNil -> 
          (LCons(h1, fun () -> LNil), LNil)
      | _ ->
          let h2 = lhd t1 in
          let t2 = ltl t1 in

          (
            LCons(h1, fun () -> fst (lpodziel t2)),
            
            LCons(h2, fun () -> snd (lpodziel t2))
          )
;;

let rec to_list n l =
  match (n, l) with
  | (0, _) -> [] 
  | (_, LNil) -> []
  | (k, LCons(x, xf)) -> x :: to_list (k-1) (xf())
;;

let rec of_list = function [] -> LNil | h::t -> LCons(h, fun () -> of_list t);;

let t1 = of_list [5;6;3;2;1];;
let (r1, r2) = lpodziel t1;;
let wynik1 = (to_list 10 r1, to_list 10 r2);;

let t2 = LNil;;
let (r3, r4) = lpodziel t2;;
let wynik2 = (to_list 10 r3, to_list 10 r4);;

let t3 = of_list [1;2;3;4];;
let (r5, r6) = lpodziel t3;;
let wynik3 = (to_list 10 r5, to_list 10 r6);;