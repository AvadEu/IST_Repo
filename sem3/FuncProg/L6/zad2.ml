type 'a tree =
  | Empty
  | Node of 'a * 'a tree * 'a tree

let rec tree_stats t =
  match t with
  | Empty -> (0, 0)
  | Node (_, left, right) ->
      let (n_left, h_left) = tree_stats left in
      let (n_right, h_right) = tree_stats right in
      
      (1 + n_left + n_right, 1 + max h_left h_right)


let t1 = Node(1, Node(2, Empty, Empty), Empty)
let t2 = Empty
let t3 = Node(1, Node(2, Empty, Empty), Node(3, Empty, Empty))
let t4 = Node(1, Empty, Node(2, Empty, Node(3, Empty, Empty)))

let res1 = tree_stats t1 (* (2, 2) *)
let res2 = tree_stats t2 (* (0, 0) *)
let res3 = tree_stats t3 (* (3, 2) *)
let res4 = tree_stats t4 (* (3, 3) *)
