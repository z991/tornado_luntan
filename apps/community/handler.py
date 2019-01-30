import os
import uuid
import json
import aiofiles

from MxForm.handler import RedisHandler
from apps.utils.mxform_decorators import authenticated_async
from apps.community.forms import CommunityGroupForm
from apps.community.models import CommunityGroup, CommunityGroupMember


class GroupHandler(RedisHandler):
    async def get(self, *args, **kwargs):
        pass
    @authenticated_async
    async def post(self, *args, **kwargs):
        re_data = {}
        print("kwargs===", self.request.files)
        print('files===', type(self.request.files), self.request.files)

        # 不能使用jsonform
        group_form = CommunityGroupForm(self.request.body_arguments)
        if group_form.validate():
            # 自己完成图片字段的认证
            files_meta = self.request.files.get("front_image", None)
            print('files_meta===', type(files_meta), files_meta)
            if not files_meta:
                self.set_status(400)
                re_data["front_image"] = "请上传图片"
            else:
                # 完成图片保存并将值设置给对应的记录
                # 通过aiofiles写文件
                # 1. 文件名
                new_filename = ""
                for meta in files_meta:
                    filename = meta["filename"]
                    # 新的文件名
                    new_filename = "{uuid}_{filename}".format(uuid=uuid.uuid1(), filename=filename)
                    # 新的文件路径
                    files_path = os.path.join(self.settings["MEDIA_ROOT"], new_filename)
                    # 将上传的文件写入到存储文件夹
                    async with aiofiles.open(files_path, 'wb') as f:
                        await f.write(meta["body"])

                group = await self.application.objects.create(CommunityGroup,
                                                              creator=self.current_user,name=group_form.name.data,
                                                              category=group_form.category.data,desc=group_form.desc.data,
                                                              notice=group_form.notice.data,from_image=new_filename)
                re_data["id"] = group.id
        else:
            self.set_status(400)
            for field in group_form.errors:
                re_data[field] = group_form.errors[field][0]
        self.finish(re_data)

class GroupDetailHanlder(RedisHandler):
    pass


class GroupMemberHandler(RedisHandler):
    pass


class PostHandler(RedisHandler):
    pass


class PostDetailHandler(RedisHandler):
    pass


class PostCommentHanlder(RedisHandler):
    pass


class CommentReplyHandler(RedisHandler):
    pass


class CommentsLikeHanlder(RedisHandler):
    pass
