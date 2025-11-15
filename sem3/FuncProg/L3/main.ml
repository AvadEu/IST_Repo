let reverse list =
  let rec reverse_in acc lst =
    match lst with
    | [] -> acc
    | head :: tail -> reverse_in (head :: acc) tail
  in
  reverse_in [] list
;;

let div list divider =
  let rec div_in acc_greater acc_smaller lst =
    match lst with
    | [] -> (acc_greater, acc_smaller)
    | head :: tail ->
        match head with
        | h when h > divider ->
            div_in (head :: acc_greater) acc_smaller tail
        | h when h < divider ->
            div_in acc_greater (head :: acc_smaller) tail
        | _ ->
            div_in acc_greater acc_smaller tail
  in
  let (reversed_greater, reversed_smaller) = div_in [] [] list in
  (reverse reversed_greater, reverse reversed_smaller) ;;

  
  div [1; 4; 2; 5; 3; 6; 3; 7] 3;;
  div [1;2;3;4;5] 40;;
  div [25; 26; 27] 20;;
  div [] 10;;
  div [-2; -1; 0; 1; 2] 0;;

