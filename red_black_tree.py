class Nil():
    # that's our black leaf 
    def __init__(self) -> None:
        self.val = None
        self.color = 0


class RedBlackNode():
    # i crate only one time this leaf
    leaf: Nil = Nil()

    def __init__(self, val: int) -> None:
        self.val = val

        self.father = None
        self.left = self.leaf
        self.right = self.leaf

        self.color = 1


class RedBlackTree():

    black: int = 0
    red: int = 1

    def __init__(self, root: RedBlackNode = None) -> None:
        self.root = root
        if self.root != None:
            self.root.color = self.black
        
    
    def insert(self, value: int) -> None:
        if self.root == None:
            self.root = RedBlackNode(value)
            # the root must be black
            self.root.color = self.black
            return 
        
        r = self.root
        while True:
            if value >= r.val:
                if r.right.val != None:
                    r = r.right
                else:
                    break
            else:
                if r.left.val != None:
                    r = r.left
                else:
                    break
        
        new_r = None
        if value >= r.val:
            r.right = RedBlackNode(value)
            r.right.father = r
            new_r = r.right
        else:
            r.left = RedBlackNode(value)
            r.left.father = r
            new_r = r.left

        self.make_control(new_r)
    

    def search(self, value: int) -> bool:
        r = self.root

        def find_value(r, value):
            if r == None or r.val == None:
                return False

            if r.val == value:
                return True

            if value < r.val:
                return find_value(r.left, value)

            if value > r.val:
                return find_value(r.right, value)

        return find_value(r, value)
    

    def find_root(self, value: int) -> RedBlackNode:
        r = self.root

        def find_value(r, value):
            if r == None or r.val == None:
                return False

            if r.val == value:
                return r

            if value < r.val:
                return find_value(r.left, value)

            if value > r.val:
                return find_value(r.right, value)

        return find_value(r, value)
    

    def make_control(self, r: RedBlackNode) -> None:
        # case 0
        # the root must be black
        if r == self.root:
            self.root.color = self.black
            return 

        father = r.father
        grand_father = father.father

        # we don't have an ucle so we can't change
        # or the color of the actually root is black
        # and we don't need to make any control
        if grand_father == None or r.color == self.black:
            self.make_control(father)
            return 

        # i like to catch the uncle and to
        # understand if "father" is the
        # right son or the left one
        if grand_father.left != father:
            uncle = grand_father.left
            father_left = False
        else:
            uncle = grand_father.right
            father_left = True
        
        # case 1
        # the father and the uncle have the
        # same color so we make it black, and 
        # the "grand_father" became red only if 
        # the father and uncle are red
        if father.color == uncle.color:
            grand_father.color = self.red if father.color == self.red else grand_father.color
            uncle.color = self.black
            father.color = self.black
            self.make_control(father)

        # case 2-3
        else:
            # try to understand if "r" is the
            # left or right son of "father"
            if r.val < father.val:
                r_left = True
            else:
                r_left = False

            #case 3
            if r_left == father_left:
                # if the father and the son ["father" and "r"]
                # are on the left/right of their father 
                # we have to do a right/left rotation from the father
                if r_left == False:
                    self.left_rotation(father)
                else:
                    self.right_rotation(father)

                # the "father" take the position of 
                # the "grand_father", and the sons of the
                # father are "r" and "grand_father",
                # "father" became black
                father.left.color = self.red
                father.right.color = self.red
                father.color = self.black

                # we re-make a control on r 
                # to check if everything is right
                self.make_control(father)

            #case 2
            else:
                # hear we make a rotation to
                # end up in case 3 at the next control
                if r_left == False:
                    self.left_rotation(r)
                else:
                    self.right_rotation(r)

                self.make_control(father)
        

    def left_rotation(self, r: RedBlackNode) -> None:
        father = r.father
        if father == self.root:
            self.root = r
        else:
            gran_father = father.father
            if father.val < gran_father.val:
                gran_father.left = r
            else:
                gran_father.right = r

        r.father = father.father
        father.right = r.left
        r.left = father

        if father.right.val != None:
            father.right.father = father
        
        father.father = r
        

    def right_rotation(self, r: RedBlackNode) -> None:
        father = r.father
        if father == self.root:
            self.root = r
        else:
            gran_father = father.father
            if father.val < gran_father.val:
                gran_father.left = r
            else:
                gran_father.right = r

        r.father = father.father
        father.left = r.right
        r.right = father
        
        if father.left.val != None:
            father.left.father = father

        father.father = r

        
    def __str__(self) -> str:

        def preorder_visit(root, lvl=0, out = ""):
            color = "B" if root.color == 0 else "R"
            out += " "*lvl + "-"*lvl + str(root.val) + " " + color + "\n"

            if root.left and root.left.val != None:
                out = preorder_visit(root.left, lvl+1, out)

            if root.right and root.right.val != None:
                out = preorder_visit(root.right, lvl+1, out)

            return out 

        return preorder_visit(self.root)