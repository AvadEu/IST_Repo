let binToDec cyfry =
  if cyfry = [] then
    raise (Failure "Lista nie moze byc pusta")
  else
  List.fold_left (fun acc bit -> (acc * 2) + bit) 0 cyfry;;


binToDec [1;1;0;1];;
binToDec [0;0;1;0;1;1];;
binToDec [1;0;1;0;1;0;1;0];;
binToDec [0;0;0;0];;
binToDec [];;
