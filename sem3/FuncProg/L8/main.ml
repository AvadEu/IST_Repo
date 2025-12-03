type llist = LNil | LCons of int * (unit -> llist)

let rec ltake n llist =
  match (n, llist) with
  | (0, _) -> []
  | (_, LNil) -> []
  | (k, LCons(x, xf)) -> x :: ltake (k-1) (xf())

let lazyFibN n =
  if n < 0 then
    failwith "n must be non-negative"
  else
  let rec fib_helper a b counter =
    if counter > n then 
      LNil
    else if (b > max_int - a) then
        failwith "Integer overflow in Fibonacci sequence"
    else
      LCons (a, fun () -> fib_helper b (a + b) (counter + 1))
  in
  fib_helper 0 1 0



let test2 = ltake 5 (lazyFibN 0);;
(* Wynik: [0] *)

let test3 = ltake 10 (lazyFibN 4);;
(* Wynik: [0; 1; 1; 2; 3] *)

let test4 = ltake 100 (lazyFibN 5);;
(* Wynik: [0; 1; 1; 2; 3; 5] *)

  let test1 = ltake 300 (lazyFibN 150);;
(* Wynik: Error *)