
def add_node(tree_dic, comment):
    if comment.parent_comment is None:
        # 如果无父评论，则放在顶层
        tree_dic[comment] = {}
    else:  # 循环当前整个dic，直到找到为止
        for k in tree_dic:
            if k == comment.parent_comment:
                # 找到父亲了
                print("find dad...", k)
                tree_dic[k][comment] = {}  # 这里会出错，因为k为一个数据对象;TypeError: keys must be a string
            else:
                print("keep going deeper....")
                # 递归继续寻找
                add_node(tree_dic[k], comment)
    print(">>>>", tree_dic)



def build_tree(comment_set):
    # 将评论通过字典转化成树结构
    print(">>>:", comment_set)
    tree_dic = {}
    for comment in comment_set:
        add_node(tree_dic, comment)
    return tree_dic


def render_tree_node(tree_dic_v, margin_val):
    html = ""
    for k in tree_dic_v:  # k为评论的数据对象
        ele = "<div class='comment-node' style='margin-left:%spx'>" % margin_val + k.comment \
              + "<span style='margin-left:20px'>%s</span>" % k.comment_date \
              + "<span style='margin-left:20px'>%s</span>" % k.comment_user \
              + '<span comment-id="%s"' % k.id + 'class="glyphicon glyphicon-comment pull-right add-comment">'\
              + "</div>"

        html += ele
        html += render_tree_node(tree_dic_v[k], margin_val+15)
    return html


def render_comment_tree(tree_dic):
    # 将字典形式的评论，转化为html字符串
    html = ""
    for k in tree_dic:
        ele = "<div class='root-comment'>" + k.comment \
              + "<span style='margin-left:20px'>%s</span>" % k.comment_date \
              + "<span style='margin-left:20px'>%s</span>" % k.comment_user \
              + '<span comment-id="%s"' % k.id + 'class="pull-right glyphicon glyphicon-comment add-comment">'\
              + "</div>"

        html += ele
        html += render_tree_node(tree_dic[k], 15)

    return html


