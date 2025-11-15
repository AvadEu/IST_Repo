let rec contains lista wartosc =
  match lista with
  | [] -> false
  | head :: reszta -> 
      if head = wartosc then
        true
      else
        contains reszta wartosc;;

let filterSublist lista wartosc =
  List.filter (fun subList -> contains subList wartosc) lista;;

filterSublist [[1;2;3];[2];[3;4];[1;2]] 2;;
filterSublist [["a";"b"];["c"];["d";"e"];["a";"c"]] "a";;
filterSublist [[true;false];[false];[true;true]] true;;

