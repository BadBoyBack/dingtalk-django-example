# encoding: utf-8
from __future__ import absolute_import, unicode_literals

from django.db import models

from core import model
from . import constants, biz


class Suite(model.BaseModel):
    suiteid = models.BigIntegerField('套件ID', null=False, blank=False)
    name = models.CharField('套件名称', max_length=256, null=False, blank=False)
    suite_key = models.CharField('套件key', max_length=128, null=False, blank=False, unique=True)
    suite_secret = models.CharField('套件secret', max_length=256, null=False, blank=False)
    token = models.CharField('套件回调token', max_length=256, null=False, blank=True, default='')
    aes_key = models.CharField('套件回调aes_key', max_length=256, null=False, blank=True, default='')

    def get_suite_client(self):
        return biz.ISVClient(self.suite_key, self.suite_secret, self.token, self.aes_key)

    class Meta:
        verbose_name = verbose_name_plural = 'ISV套件'


class Corp(model.BaseModel):
    corpid = models.CharField('授权方企业id', max_length=128, unique=True)
    status = models.IntegerField('授权状态', choices=(constants.CORP_AUTH_LEVEL_CODE.get_list()),
                                 default=constants.CORP_AUTH_LEVEL_CODE.NO.code, null=False, blank=True)
    corp_name = models.CharField('授权方企业名称', max_length=256, null=False, blank=True)
    invite_code = models.CharField('邀请码', max_length=256, null=False, blank=True)
    industry = models.CharField('企业所属行业', max_length=256, null=False, blank=True)
    license_code = models.CharField('序列号', max_length=256, null=False, blank=True)
    auth_channel = models.CharField('渠道码', max_length=256, null=False, blank=True)
    auth_channel_type = models.CharField('渠道类型', max_length=256, null=False, blank=True)
    is_authenticated = models.BooleanField('企业是否认证', null=False, blank=True, default=False)
    auth_level = models.IntegerField('企业认证等级', choices=(constants.CORP_AUTH_LEVEL_CODE.get_list()),
                                     default=constants.CORP_AUTH_LEVEL_CODE.NO.code, null=False, blank=True)
    invite_url = models.CharField('企业邀请链接', max_length=1024, null=False, blank=True)
    corp_logo_url = models.ImageField('企业logo', max_length=1024, null=False, blank=True)

    permanent_code = models.CharField('永久授权码', max_length=1024, null=False, blank=True)
    ch_permanent_code = models.CharField('企业服务窗永久授权码', max_length=1024, null=False, blank=True)
    suite = model.ForeignKey(
        Suite,
        to_field='suite_key',
        verbose_name='所属套件',
        db_constraint=False,
        db_column='suite_key',
        null=False,
        on_delete=models.DO_NOTHING
    )

    class Meta:
        unique_together = ('corpid', 'suite')
        verbose_name = verbose_name_plural = '企业信息'

#
# class Agent(model.BaseModel):
#     agentid = models.BigIntegerField('应用id', null=False, blank=False)
#     name = models.CharField('应用名称', max_length=256, null=False, blank=True)
#     logo_url = models.ImageField('应用头像', max_length=1024, null=False, blank=True)
#     description = models.CharField('应用详情')
#     close = models.IntegerField('是否被禁用', choices=(constants.AGENT_CLOSE_CODE.get_list()),
#                                 default=constants.AGENT_CLOSE_CODE.FORBIDDEN, null=False, blank=False)
#     corp = model.ForeignKey(
#         Corp,
#         to_field='corpid',
#         verbose_name='企业',
#         db_constraint=False,
#         db_column='corpid',
#         null=False,
#         on_delete=models.DO_NOTHING
#     )
#
#     class Meta:
#         unique_together = ('agentid', 'corp')
#         verbose_name = verbose_name_plural = '企业应用信息'
