let rec genlist a b = if a > b then genlist b a else (if a == b then [a] else a :: genlist (a + 1) b);;

let rec odliczanie n = if n < 1 then [] else n :: odliczanie (n - 1);;

let rec iloczyn a  = if a == [] then 1 else List.hd a * iloczyn (List.tl a);;