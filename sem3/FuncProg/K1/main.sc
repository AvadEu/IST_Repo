def sum(arr: List[(Int, Int)]): List[(Int, Int)] = {
  def help(acc_a: Int, acc_b: Int, arr: List[(Int, Int)]): List[(Int, Int)] = {
    arr match {
      case Nil => List((acc_a, acc_b))
      case (x, y) :: t => help(acc_a + x, acc_b + y, t)
    }
  }
  help(0, 0, arr)
}