let reverse lista =
  let rec reverse_in acc l =
    match l with
    | [] -> acc
    | h :: t -> reverse_in (h :: acc) t
  in
  reverse_in [] lista
;;

let parse lista_wejsciowa =
  let rec parse_in (l10, l5, inne) reszta =
    match reszta with
    | [] -> (l10, l5, inne)    
    | h :: t ->
        if h mod 10 = 0 then
          parse_in (h :: l10, h :: l5, inne) t
        else if h mod 5 = 0 then
          parse_in (l10, h :: l5, inne) t
        else
          parse_in (l10, l5, h :: inne) t
  in
  let (rev_l10, rev_l5, rev_inne) = 
    parse_in ([], [], []) lista_wejsciowa 
  in
  (reverse rev_l10, reverse rev_l5, reverse rev_inne)
;;



parse [20;21;25;30;40];;
parse [];;
parse [1;2;3];;
parse [10; 15];;