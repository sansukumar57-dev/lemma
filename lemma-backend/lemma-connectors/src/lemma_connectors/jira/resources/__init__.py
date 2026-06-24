from __future__ import annotations

from lemma_connectors.jira.resources.accessible_project_type_by_key import JiraAccessibleProjectTypeByKeyResource
from lemma_connectors.jira.resources.actor import JiraActorResource
from lemma_connectors.jira.resources.actor_users import JiraActorUsersResource
from lemma_connectors.jira.resources.actors import JiraActorsResource
from lemma_connectors.jira.resources.addon_properties_resource import JiraAddonPropertiesResourceResource
from lemma_connectors.jira.resources.advanced_settings import JiraAdvancedSettingsResource
from lemma_connectors.jira.resources.all_accessible_project_types import JiraAllAccessibleProjectTypesResource
from lemma_connectors.jira.resources.all_application_roles import JiraAllApplicationRolesResource
from lemma_connectors.jira.resources.all_available_dashboard_gadgets import JiraAllAvailableDashboardGadgetsResource
from lemma_connectors.jira.resources.all_dashboards import JiraAllDashboardsResource
from lemma_connectors.jira.resources.all_field_configuration_schemes import JiraAllFieldConfigurationSchemesResource
from lemma_connectors.jira.resources.all_field_configurations import JiraAllFieldConfigurationsResource
from lemma_connectors.jira.resources.all_gadgets import JiraAllGadgetsResource
from lemma_connectors.jira.resources.all_issue_field_options import JiraAllIssueFieldOptionsResource
from lemma_connectors.jira.resources.all_issue_type_schemes import JiraAllIssueTypeSchemesResource
from lemma_connectors.jira.resources.all_labels import JiraAllLabelsResource
from lemma_connectors.jira.resources.all_permission_schemes import JiraAllPermissionSchemesResource
from lemma_connectors.jira.resources.all_permissions import JiraAllPermissionsResource
from lemma_connectors.jira.resources.all_project_avatars import JiraAllProjectAvatarsResource
from lemma_connectors.jira.resources.all_project_categories import JiraAllProjectCategoriesResource
from lemma_connectors.jira.resources.all_project_roles import JiraAllProjectRolesResource
from lemma_connectors.jira.resources.all_project_types import JiraAllProjectTypesResource
from lemma_connectors.jira.resources.all_projects import JiraAllProjectsResource
from lemma_connectors.jira.resources.all_screen_tab_fields import JiraAllScreenTabFieldsResource
from lemma_connectors.jira.resources.all_screen_tabs import JiraAllScreenTabsResource
from lemma_connectors.jira.resources.all_statuses import JiraAllStatusesResource
from lemma_connectors.jira.resources.all_system_avatars import JiraAllSystemAvatarsResource
from lemma_connectors.jira.resources.all_users import JiraAllUsersResource
from lemma_connectors.jira.resources.all_users_default import JiraAllUsersDefaultResource
from lemma_connectors.jira.resources.all_workflow_schemes import JiraAllWorkflowSchemesResource
from lemma_connectors.jira.resources.all_workflows import JiraAllWorkflowsResource
from lemma_connectors.jira.resources.alternative_issue_types import JiraAlternativeIssueTypesResource
from lemma_connectors.jira.resources.analyse import JiraAnalyseResource
from lemma_connectors.jira.resources.and_replace_version import JiraAndReplaceVersionResource
from lemma_connectors.jira.resources.app_issue_field_value_update_resource import JiraAppIssueFieldValueUpdateResourceResource
from lemma_connectors.jira.resources.application_property import JiraApplicationPropertyResource
from lemma_connectors.jira.resources.application_role import JiraApplicationRoleResource
from lemma_connectors.jira.resources.approximate_application_license_count import JiraApproximateApplicationLicenseCountResource
from lemma_connectors.jira.resources.approximate_license_count import JiraApproximateLicenseCountResource
from lemma_connectors.jira.resources.assign import JiraAssignResource
from lemma_connectors.jira.resources.assign_field_configuration_scheme_to import JiraAssignFieldConfigurationSchemeToResource
from lemma_connectors.jira.resources.assign_issue_type_scheme_to import JiraAssignIssueTypeSchemeToResource
from lemma_connectors.jira.resources.assign_issue_type_screen_scheme_to import JiraAssignIssueTypeScreenSchemeToResource
from lemma_connectors.jira.resources.assign_permission import JiraAssignPermissionResource
from lemma_connectors.jira.resources.assign_projects_to_custom_field import JiraAssignProjectsToCustomFieldResource
from lemma_connectors.jira.resources.assign_scheme_to import JiraAssignSchemeToResource
from lemma_connectors.jira.resources.assigned_permission_scheme import JiraAssignedPermissionSchemeResource
from lemma_connectors.jira.resources.attachment import JiraAttachmentResource
from lemma_connectors.jira.resources.attachment_content import JiraAttachmentContentResource
from lemma_connectors.jira.resources.attachment_for_humans import JiraAttachmentForHumansResource
from lemma_connectors.jira.resources.attachment_for_machines import JiraAttachmentForMachinesResource
from lemma_connectors.jira.resources.attachment_meta import JiraAttachmentMetaResource
from lemma_connectors.jira.resources.attachment_thumbnail import JiraAttachmentThumbnailResource
from lemma_connectors.jira.resources.audit_records import JiraAuditRecordsResource
from lemma_connectors.jira.resources.auto_complete import JiraAutoCompleteResource
from lemma_connectors.jira.resources.auto_complete_post import JiraAutoCompletePostResource
from lemma_connectors.jira.resources.available_screen_fields import JiraAvailableScreenFieldsResource
from lemma_connectors.jira.resources.available_time_tracking_implementations import JiraAvailableTimeTrackingImplementationsResource
from lemma_connectors.jira.resources.avatar import JiraAvatarResource
from lemma_connectors.jira.resources.avatar_image_by_id import JiraAvatarImageByIdResource
from lemma_connectors.jira.resources.avatar_image_by_owner import JiraAvatarImageByOwnerResource
from lemma_connectors.jira.resources.avatar_image_by_type import JiraAvatarImageByTypeResource
from lemma_connectors.jira.resources.avatars import JiraAvatarsResource
from lemma_connectors.jira.resources.banner import JiraBannerResource
from lemma_connectors.jira.resources.bulk_delete_issue import JiraBulkDeleteIssueResource
from lemma_connectors.jira.resources.bulk_get import JiraBulkGetResource
from lemma_connectors.jira.resources.bulk_get_users import JiraBulkGetUsersResource
from lemma_connectors.jira.resources.bulk_permissions import JiraBulkPermissionsResource
from lemma_connectors.jira.resources.bulk_set_issue import JiraBulkSetIssueResource
from lemma_connectors.jira.resources.bulk_set_issue_properties_by import JiraBulkSetIssuePropertiesByResource
from lemma_connectors.jira.resources.bulk_set_issues_properties import JiraBulkSetIssuesPropertiesResource
from lemma_connectors.jira.resources.cancel import JiraCancelResource
from lemma_connectors.jira.resources.change_filter import JiraChangeFilterResource
from lemma_connectors.jira.resources.change_logs import JiraChangeLogsResource
from lemma_connectors.jira.resources.change_logs_by_ids import JiraChangeLogsByIdsResource
from lemma_connectors.jira.resources.columns import JiraColumnsResource
from lemma_connectors.jira.resources.comment import JiraCommentResource
from lemma_connectors.jira.resources.comment_property import JiraCommentPropertyResource
from lemma_connectors.jira.resources.comment_property_keys import JiraCommentPropertyKeysResource
from lemma_connectors.jira.resources.comments import JiraCommentsResource
from lemma_connectors.jira.resources.comments_by_ids import JiraCommentsByIdsResource
from lemma_connectors.jira.resources.component import JiraComponentResource
from lemma_connectors.jira.resources.component_related_issues import JiraComponentRelatedIssuesResource
from lemma_connectors.jira.resources.configuration import JiraConfigurationResource
from lemma_connectors.jira.resources.contexts_for_field import JiraContextsForFieldResource
from lemma_connectors.jira.resources.contexts_for_field_deprecated import JiraContextsForFieldDeprecatedResource
from lemma_connectors.jira.resources.create_issue_meta import JiraCreateIssueMetaResource
from lemma_connectors.jira.resources.current_user import JiraCurrentUserResource
from lemma_connectors.jira.resources.custom_field import JiraCustomFieldResource
from lemma_connectors.jira.resources.custom_field_configuration import JiraCustomFieldConfigurationResource
from lemma_connectors.jira.resources.custom_field_context import JiraCustomFieldContextResource
from lemma_connectors.jira.resources.custom_field_context_from_projects import JiraCustomFieldContextFromProjectsResource
from lemma_connectors.jira.resources.custom_field_contexts_for_projects_and_issue_types import JiraCustomFieldContextsForProjectsAndIssueTypesResource
from lemma_connectors.jira.resources.custom_field_option import JiraCustomFieldOptionResource
from lemma_connectors.jira.resources.custom_field_value import JiraCustomFieldValueResource
from lemma_connectors.jira.resources.dashboard import JiraDashboardResource
from lemma_connectors.jira.resources.dashboard_item_property import JiraDashboardItemPropertyResource
from lemma_connectors.jira.resources.dashboard_item_property_keys import JiraDashboardItemPropertyKeysResource
from lemma_connectors.jira.resources.dashboards_paginated import JiraDashboardsPaginatedResource
from lemma_connectors.jira.resources.default_priority import JiraDefaultPriorityResource
from lemma_connectors.jira.resources.default_resolution import JiraDefaultResolutionResource
from lemma_connectors.jira.resources.default_screen_scheme import JiraDefaultScreenSchemeResource
from lemma_connectors.jira.resources.default_share_scope import JiraDefaultShareScopeResource
from lemma_connectors.jira.resources.default_values import JiraDefaultValuesResource
from lemma_connectors.jira.resources.default_workflow import JiraDefaultWorkflowResource
from lemma_connectors.jira.resources.do import JiraDoResource
from lemma_connectors.jira.resources.draft_default_workflow import JiraDraftDefaultWorkflowResource
from lemma_connectors.jira.resources.draft_workflow import JiraDraftWorkflowResource
from lemma_connectors.jira.resources.draft_workflow_mapping import JiraDraftWorkflowMappingResource
from lemma_connectors.jira.resources.dynamic_modules_resource import JiraDynamicModulesResourceResource
from lemma_connectors.jira.resources.dynamic_webhooks_for_app import JiraDynamicWebhooksForAppResource
from lemma_connectors.jira.resources.edit import JiraEditResource
from lemma_connectors.jira.resources.edit_issue_meta import JiraEditIssueMetaResource
from lemma_connectors.jira.resources.evaluate_jira import JiraEvaluateJiraResource
from lemma_connectors.jira.resources.events import JiraEventsResource
from lemma_connectors.jira.resources.failed_webhooks import JiraFailedWebhooksResource
from lemma_connectors.jira.resources.favourite_filters import JiraFavouriteFiltersResource
from lemma_connectors.jira.resources.favourite_for_filter import JiraFavouriteForFilterResource
from lemma_connectors.jira.resources.features_for_project import JiraFeaturesForProjectResource
from lemma_connectors.jira.resources.field_auto_complete_for_query_string import JiraFieldAutoCompleteForQueryStringResource
from lemma_connectors.jira.resources.field_configuration import JiraFieldConfigurationResource
from lemma_connectors.jira.resources.field_configuration_items import JiraFieldConfigurationItemsResource
from lemma_connectors.jira.resources.field_configuration_scheme import JiraFieldConfigurationSchemeResource
from lemma_connectors.jira.resources.field_configuration_scheme_mapping import JiraFieldConfigurationSchemeMappingResource
from lemma_connectors.jira.resources.field_configuration_scheme_mappings import JiraFieldConfigurationSchemeMappingsResource
from lemma_connectors.jira.resources.field_configuration_scheme_project_mapping import JiraFieldConfigurationSchemeProjectMappingResource
from lemma_connectors.jira.resources.field_to_default_screen import JiraFieldToDefaultScreenResource
from lemma_connectors.jira.resources.fields import JiraFieldsResource
from lemma_connectors.jira.resources.fields_paginated import JiraFieldsPaginatedResource
from lemma_connectors.jira.resources.filter import JiraFilterResource
from lemma_connectors.jira.resources.filters import JiraFiltersResource
from lemma_connectors.jira.resources.filters_paginated import JiraFiltersPaginatedResource
from lemma_connectors.jira.resources.find import JiraFindResource
from lemma_connectors.jira.resources.find_assignable import JiraFindAssignableResource
from lemma_connectors.jira.resources.find_bulk_assignable import JiraFindBulkAssignableResource
from lemma_connectors.jira.resources.find_user_keys_by import JiraFindUserKeysByResource
from lemma_connectors.jira.resources.find_users_and import JiraFindUsersAndResource
from lemma_connectors.jira.resources.find_users_by import JiraFindUsersByResource
from lemma_connectors.jira.resources.find_users_for import JiraFindUsersForResource
from lemma_connectors.jira.resources.find_users_with_all import JiraFindUsersWithAllResource
from lemma_connectors.jira.resources.find_users_with_browse import JiraFindUsersWithBrowseResource
from lemma_connectors.jira.resources.for_issues_using_jql import JiraForIssuesUsingJqlResource
from lemma_connectors.jira.resources.for_issues_using_jql_post import JiraForIssuesUsingJqlPostResource
from lemma_connectors.jira.resources.fully_update_project import JiraFullyUpdateProjectResource
from lemma_connectors.jira.resources.gadget import JiraGadgetResource
from lemma_connectors.jira.resources.group import JiraGroupResource
from lemma_connectors.jira.resources.hierarchy import JiraHierarchyResource
from lemma_connectors.jira.resources.ids_of_worklogs_deleted_since import JiraIdsOfWorklogsDeletedSinceResource
from lemma_connectors.jira.resources.ids_of_worklogs_modified_since import JiraIdsOfWorklogsModifiedSinceResource
from lemma_connectors.jira.resources.inactive_workflow import JiraInactiveWorkflowResource
from lemma_connectors.jira.resources.is_watching_issue_bulk import JiraIsWatchingIssueBulkResource
from lemma_connectors.jira.resources.issue import JiraIssueResource
from lemma_connectors.jira.resources.issue_all_types import JiraIssueAllTypesResource
from lemma_connectors.jira.resources.issue_field_option import JiraIssueFieldOptionResource
from lemma_connectors.jira.resources.issue_link import JiraIssueLinkResource
from lemma_connectors.jira.resources.issue_link_type import JiraIssueLinkTypeResource
from lemma_connectors.jira.resources.issue_link_types import JiraIssueLinkTypesResource
from lemma_connectors.jira.resources.issue_navigator_default_columns import JiraIssueNavigatorDefaultColumnsResource
from lemma_connectors.jira.resources.issue_picker_resource import JiraIssuePickerResourceResource
from lemma_connectors.jira.resources.issue_property import JiraIssuePropertyResource
from lemma_connectors.jira.resources.issue_property_keys import JiraIssuePropertyKeysResource
from lemma_connectors.jira.resources.issue_security_level import JiraIssueSecurityLevelResource
from lemma_connectors.jira.resources.issue_security_level_members import JiraIssueSecurityLevelMembersResource
from lemma_connectors.jira.resources.issue_security_scheme import JiraIssueSecuritySchemeResource
from lemma_connectors.jira.resources.issue_security_schemes import JiraIssueSecuritySchemesResource
from lemma_connectors.jira.resources.issue_type import JiraIssueTypeResource
from lemma_connectors.jira.resources.issue_type_avatar import JiraIssueTypeAvatarResource
from lemma_connectors.jira.resources.issue_type_from_issue_type_scheme import JiraIssueTypeFromIssueTypeSchemeResource
from lemma_connectors.jira.resources.issue_type_mappings_for_contexts import JiraIssueTypeMappingsForContextsResource
from lemma_connectors.jira.resources.issue_type_property import JiraIssueTypePropertyResource
from lemma_connectors.jira.resources.issue_type_property_keys import JiraIssueTypePropertyKeysResource
from lemma_connectors.jira.resources.issue_type_scheme import JiraIssueTypeSchemeResource
from lemma_connectors.jira.resources.issue_type_scheme_for_projects import JiraIssueTypeSchemeForProjectsResource
from lemma_connectors.jira.resources.issue_type_schemes_mapping import JiraIssueTypeSchemesMappingResource
from lemma_connectors.jira.resources.issue_type_screen_scheme import JiraIssueTypeScreenSchemeResource
from lemma_connectors.jira.resources.issue_type_screen_scheme_mappings import JiraIssueTypeScreenSchemeMappingsResource
from lemma_connectors.jira.resources.issue_type_screen_scheme_project_associations import JiraIssueTypeScreenSchemeProjectAssociationsResource
from lemma_connectors.jira.resources.issue_type_screen_schemes import JiraIssueTypeScreenSchemesResource
from lemma_connectors.jira.resources.issue_types_for_project import JiraIssueTypesForProjectResource
from lemma_connectors.jira.resources.issue_types_from_context import JiraIssueTypesFromContextResource
from lemma_connectors.jira.resources.issue_types_from_global_field_configuration_scheme import JiraIssueTypesFromGlobalFieldConfigurationSchemeResource
from lemma_connectors.jira.resources.issue_types_to_context import JiraIssueTypesToContextResource
from lemma_connectors.jira.resources.issue_types_to_issue_type_scheme import JiraIssueTypesToIssueTypeSchemeResource
from lemma_connectors.jira.resources.issue_watchers import JiraIssueWatchersResource
from lemma_connectors.jira.resources.issue_worklog import JiraIssueWorklogResource
from lemma_connectors.jira.resources.issues import JiraIssuesResource
from lemma_connectors.jira.resources.license import JiraLicenseResource
from lemma_connectors.jira.resources.link import JiraLinkResource
from lemma_connectors.jira.resources.locale import JiraLocaleResource
from lemma_connectors.jira.resources.mappings_for_issue_type_screen_scheme import JiraMappingsForIssueTypeScreenSchemeResource
from lemma_connectors.jira.resources.mappings_from_issue_type_screen_scheme import JiraMappingsFromIssueTypeScreenSchemeResource
from lemma_connectors.jira.resources.match import JiraMatchResource
from lemma_connectors.jira.resources.merge import JiraMergeResource
from lemma_connectors.jira.resources.migrate import JiraMigrateResource
from lemma_connectors.jira.resources.migration_resource import JiraMigrationResourceResource
from lemma_connectors.jira.resources.multiple_custom_field_values import JiraMultipleCustomFieldValuesResource
from lemma_connectors.jira.resources.my_filters import JiraMyFiltersResource
from lemma_connectors.jira.resources.my_permissions import JiraMyPermissionsResource
from lemma_connectors.jira.resources.notification_from_notification_scheme import JiraNotificationFromNotificationSchemeResource
from lemma_connectors.jira.resources.notification_scheme import JiraNotificationSchemeResource
from lemma_connectors.jira.resources.notification_scheme_for_project import JiraNotificationSchemeForProjectResource
from lemma_connectors.jira.resources.notification_scheme_to_project_mappings import JiraNotificationSchemeToProjectMappingsResource
from lemma_connectors.jira.resources.notification_schemes import JiraNotificationSchemesResource
from lemma_connectors.jira.resources.notifications import JiraNotificationsResource
from lemma_connectors.jira.resources.options_for_context import JiraOptionsForContextResource
from lemma_connectors.jira.resources.or_update_remote_issue_link import JiraOrUpdateRemoteIssueLinkResource
from lemma_connectors.jira.resources.parse_jql import JiraParseJqlResource
from lemma_connectors.jira.resources.partial_update_project import JiraPartialUpdateProjectResource
from lemma_connectors.jira.resources.permission_grant import JiraPermissionGrantResource
from lemma_connectors.jira.resources.permission_scheme import JiraPermissionSchemeResource
from lemma_connectors.jira.resources.permission_scheme_entity import JiraPermissionSchemeEntityResource
from lemma_connectors.jira.resources.permission_scheme_grant import JiraPermissionSchemeGrantResource
from lemma_connectors.jira.resources.permission_scheme_grants import JiraPermissionSchemeGrantsResource
from lemma_connectors.jira.resources.permitted_projects import JiraPermittedProjectsResource
from lemma_connectors.jira.resources.precomputations import JiraPrecomputationsResource
from lemma_connectors.jira.resources.preference import JiraPreferenceResource
from lemma_connectors.jira.resources.priorities import JiraPrioritiesResource
from lemma_connectors.jira.resources.priority import JiraPriorityResource
from lemma_connectors.jira.resources.project import JiraProjectResource
from lemma_connectors.jira.resources.project_asynchronously import JiraProjectAsynchronouslyResource
from lemma_connectors.jira.resources.project_avatar import JiraProjectAvatarResource
from lemma_connectors.jira.resources.project_category import JiraProjectCategoryResource
from lemma_connectors.jira.resources.project_category_by_id import JiraProjectCategoryByIdResource
from lemma_connectors.jira.resources.project_components import JiraProjectComponentsResource
from lemma_connectors.jira.resources.project_components_paginated import JiraProjectComponentsPaginatedResource
from lemma_connectors.jira.resources.project_context_mapping import JiraProjectContextMappingResource
from lemma_connectors.jira.resources.project_email import JiraProjectEmailResource
from lemma_connectors.jira.resources.project_issue_security_scheme import JiraProjectIssueSecuritySchemeResource
from lemma_connectors.jira.resources.project_property import JiraProjectPropertyResource
from lemma_connectors.jira.resources.project_property_keys import JiraProjectPropertyKeysResource
from lemma_connectors.jira.resources.project_role import JiraProjectRoleResource
from lemma_connectors.jira.resources.project_role_actors_for_role import JiraProjectRoleActorsForRoleResource
from lemma_connectors.jira.resources.project_role_actors_from_role import JiraProjectRoleActorsFromRoleResource
from lemma_connectors.jira.resources.project_role_actors_to_role import JiraProjectRoleActorsToRoleResource
from lemma_connectors.jira.resources.project_role_by_id import JiraProjectRoleByIdResource
from lemma_connectors.jira.resources.project_role_details import JiraProjectRoleDetailsResource
from lemma_connectors.jira.resources.project_roles import JiraProjectRolesResource
from lemma_connectors.jira.resources.project_type import JiraProjectTypeResource
from lemma_connectors.jira.resources.project_type_by_key import JiraProjectTypeByKeyResource
from lemma_connectors.jira.resources.project_versions import JiraProjectVersionsResource
from lemma_connectors.jira.resources.project_versions_paginated import JiraProjectVersionsPaginatedResource
from lemma_connectors.jira.resources.projects import JiraProjectsResource
from lemma_connectors.jira.resources.projects_for_issue_type_screen_scheme import JiraProjectsForIssueTypeScreenSchemeResource
from lemma_connectors.jira.resources.publish_draft_workflow import JiraPublishDraftWorkflowResource
from lemma_connectors.jira.resources.recent import JiraRecentResource
from lemma_connectors.jira.resources.refresh import JiraRefreshResource
from lemma_connectors.jira.resources.register_dynamic import JiraRegisterDynamicResource
from lemma_connectors.jira.resources.remote_issue_link import JiraRemoteIssueLinkResource
from lemma_connectors.jira.resources.remote_issue_link_by_global_id import JiraRemoteIssueLinkByGlobalIdResource
from lemma_connectors.jira.resources.remote_issue_link_by_id import JiraRemoteIssueLinkByIdResource
from lemma_connectors.jira.resources.remote_issue_links import JiraRemoteIssueLinksResource
from lemma_connectors.jira.resources.reorder_custom_field import JiraReorderCustomFieldResource
from lemma_connectors.jira.resources.reorder_issue_types_in_issue_type import JiraReorderIssueTypesInIssueTypeResource
from lemma_connectors.jira.resources.replace_issue_field import JiraReplaceIssueFieldResource
from lemma_connectors.jira.resources.reset import JiraResetResource
from lemma_connectors.jira.resources.reset_user import JiraResetUserResource
from lemma_connectors.jira.resources.resolution import JiraResolutionResource
from lemma_connectors.jira.resources.resolutions import JiraResolutionsResource
from lemma_connectors.jira.resources.root import JiraRootResource
from lemma_connectors.jira.resources.sanitise_jql import JiraSanitiseJqlResource
from lemma_connectors.jira.resources.screen import JiraScreenResource
from lemma_connectors.jira.resources.screen_scheme import JiraScreenSchemeResource
from lemma_connectors.jira.resources.screen_schemes import JiraScreenSchemesResource
from lemma_connectors.jira.resources.screen_tab import JiraScreenTabResource
from lemma_connectors.jira.resources.screen_tab_field import JiraScreenTabFieldResource
from lemma_connectors.jira.resources.screens import JiraScreensResource
from lemma_connectors.jira.resources.screens_for_field import JiraScreensForFieldResource
from lemma_connectors.jira.resources.security_levels_for_project import JiraSecurityLevelsForProjectResource
from lemma_connectors.jira.resources.select_time_tracking import JiraSelectTimeTrackingResource
from lemma_connectors.jira.resources.selectable_issue_field_options import JiraSelectableIssueFieldOptionsResource
from lemma_connectors.jira.resources.selected_time_tracking_implementation import JiraSelectedTimeTrackingImplementationResource
from lemma_connectors.jira.resources.server_info import JiraServerInfoResource
from lemma_connectors.jira.resources.share_permission import JiraSharePermissionResource
from lemma_connectors.jira.resources.share_permissions import JiraSharePermissionsResource
from lemma_connectors.jira.resources.shared_time_tracking_configuration import JiraSharedTimeTrackingConfigurationResource
from lemma_connectors.jira.resources.status import JiraStatusResource
from lemma_connectors.jira.resources.status_categories import JiraStatusCategoriesResource
from lemma_connectors.jira.resources.status_category import JiraStatusCategoryResource
from lemma_connectors.jira.resources.statuses import JiraStatusesResource
from lemma_connectors.jira.resources.statuses_by_id import JiraStatusesByIdResource
from lemma_connectors.jira.resources.store import JiraStoreResource
from lemma_connectors.jira.resources.task import JiraTaskResource
from lemma_connectors.jira.resources.toggle_feature_for import JiraToggleFeatureForResource
from lemma_connectors.jira.resources.transitions import JiraTransitionsResource
from lemma_connectors.jira.resources.trashed_fields_paginated import JiraTrashedFieldsPaginatedResource
from lemma_connectors.jira.resources.ui_modification import JiraUiModificationResource
from lemma_connectors.jira.resources.ui_modifications import JiraUiModificationsResource
from lemma_connectors.jira.resources.user import JiraUserResource
from lemma_connectors.jira.resources.user_columns import JiraUserColumnsResource
from lemma_connectors.jira.resources.user_default_columns import JiraUserDefaultColumnsResource
from lemma_connectors.jira.resources.user_email import JiraUserEmailResource
from lemma_connectors.jira.resources.user_email_bulk import JiraUserEmailBulkResource
from lemma_connectors.jira.resources.user_from_group import JiraUserFromGroupResource
from lemma_connectors.jira.resources.user_groups import JiraUserGroupsResource
from lemma_connectors.jira.resources.user_property import JiraUserPropertyResource
from lemma_connectors.jira.resources.user_property_keys import JiraUserPropertyKeysResource
from lemma_connectors.jira.resources.user_to_group import JiraUserToGroupResource
from lemma_connectors.jira.resources.users_from_group import JiraUsersFromGroupResource
from lemma_connectors.jira.resources.valid_project_key import JiraValidProjectKeyResource
from lemma_connectors.jira.resources.valid_project_name import JiraValidProjectNameResource
from lemma_connectors.jira.resources.validate_project import JiraValidateProjectResource
from lemma_connectors.jira.resources.version import JiraVersionResource
from lemma_connectors.jira.resources.version_related_issues import JiraVersionRelatedIssuesResource
from lemma_connectors.jira.resources.version_unresolved_issues import JiraVersionUnresolvedIssuesResource
from lemma_connectors.jira.resources.visible_issue_field_options import JiraVisibleIssueFieldOptionsResource
from lemma_connectors.jira.resources.vote import JiraVoteResource
from lemma_connectors.jira.resources.votes import JiraVotesResource
from lemma_connectors.jira.resources.watcher import JiraWatcherResource
from lemma_connectors.jira.resources.webhook_by_id import JiraWebhookByIdResource
from lemma_connectors.jira.resources.workflow import JiraWorkflowResource
from lemma_connectors.jira.resources.workflow_mapping import JiraWorkflowMappingResource
from lemma_connectors.jira.resources.workflow_scheme import JiraWorkflowSchemeResource
from lemma_connectors.jira.resources.workflow_scheme_draft import JiraWorkflowSchemeDraftResource
from lemma_connectors.jira.resources.workflow_scheme_draft_from_parent import JiraWorkflowSchemeDraftFromParentResource
from lemma_connectors.jira.resources.workflow_scheme_draft_issue_type import JiraWorkflowSchemeDraftIssueTypeResource
from lemma_connectors.jira.resources.workflow_scheme_issue_type import JiraWorkflowSchemeIssueTypeResource
from lemma_connectors.jira.resources.workflow_scheme_project_associations import JiraWorkflowSchemeProjectAssociationsResource
from lemma_connectors.jira.resources.workflow_transition_properties import JiraWorkflowTransitionPropertiesResource
from lemma_connectors.jira.resources.workflow_transition_property import JiraWorkflowTransitionPropertyResource
from lemma_connectors.jira.resources.workflow_transition_rule_configurations import JiraWorkflowTransitionRuleConfigurationsResource
from lemma_connectors.jira.resources.workflows_paginated import JiraWorkflowsPaginatedResource
from lemma_connectors.jira.resources.worklog import JiraWorklogResource
from lemma_connectors.jira.resources.worklog_property import JiraWorklogPropertyResource
from lemma_connectors.jira.resources.worklog_property_keys import JiraWorklogPropertyKeysResource
from lemma_connectors.jira.resources.worklogs_for_ids import JiraWorklogsForIdsResource


def build_resources(client):
    return {
        'accessible_project_type_by_key': JiraAccessibleProjectTypeByKeyResource(client),
        'actor': JiraActorResource(client),
        'actor_users': JiraActorUsersResource(client),
        'actors': JiraActorsResource(client),
        'addon_properties_resource': JiraAddonPropertiesResourceResource(client),
        'advanced_settings': JiraAdvancedSettingsResource(client),
        'all_accessible_project_types': JiraAllAccessibleProjectTypesResource(client),
        'all_application_roles': JiraAllApplicationRolesResource(client),
        'all_available_dashboard_gadgets': JiraAllAvailableDashboardGadgetsResource(client),
        'all_dashboards': JiraAllDashboardsResource(client),
        'all_field_configuration_schemes': JiraAllFieldConfigurationSchemesResource(client),
        'all_field_configurations': JiraAllFieldConfigurationsResource(client),
        'all_gadgets': JiraAllGadgetsResource(client),
        'all_issue_field_options': JiraAllIssueFieldOptionsResource(client),
        'all_issue_type_schemes': JiraAllIssueTypeSchemesResource(client),
        'all_labels': JiraAllLabelsResource(client),
        'all_permission_schemes': JiraAllPermissionSchemesResource(client),
        'all_permissions': JiraAllPermissionsResource(client),
        'all_project_avatars': JiraAllProjectAvatarsResource(client),
        'all_project_categories': JiraAllProjectCategoriesResource(client),
        'all_project_roles': JiraAllProjectRolesResource(client),
        'all_project_types': JiraAllProjectTypesResource(client),
        'all_projects': JiraAllProjectsResource(client),
        'all_screen_tab_fields': JiraAllScreenTabFieldsResource(client),
        'all_screen_tabs': JiraAllScreenTabsResource(client),
        'all_statuses': JiraAllStatusesResource(client),
        'all_system_avatars': JiraAllSystemAvatarsResource(client),
        'all_users': JiraAllUsersResource(client),
        'all_users_default': JiraAllUsersDefaultResource(client),
        'all_workflow_schemes': JiraAllWorkflowSchemesResource(client),
        'all_workflows': JiraAllWorkflowsResource(client),
        'alternative_issue_types': JiraAlternativeIssueTypesResource(client),
        'analyse': JiraAnalyseResource(client),
        'and_replace_version': JiraAndReplaceVersionResource(client),
        'app_issue_field_value_update_resource': JiraAppIssueFieldValueUpdateResourceResource(client),
        'application_property': JiraApplicationPropertyResource(client),
        'application_role': JiraApplicationRoleResource(client),
        'approximate_application_license_count': JiraApproximateApplicationLicenseCountResource(client),
        'approximate_license_count': JiraApproximateLicenseCountResource(client),
        'assign': JiraAssignResource(client),
        'assign_field_configuration_scheme_to': JiraAssignFieldConfigurationSchemeToResource(client),
        'assign_issue_type_scheme_to': JiraAssignIssueTypeSchemeToResource(client),
        'assign_issue_type_screen_scheme_to': JiraAssignIssueTypeScreenSchemeToResource(client),
        'assign_permission': JiraAssignPermissionResource(client),
        'assign_projects_to_custom_field': JiraAssignProjectsToCustomFieldResource(client),
        'assign_scheme_to': JiraAssignSchemeToResource(client),
        'assigned_permission_scheme': JiraAssignedPermissionSchemeResource(client),
        'attachment': JiraAttachmentResource(client),
        'attachment_content': JiraAttachmentContentResource(client),
        'attachment_for_humans': JiraAttachmentForHumansResource(client),
        'attachment_for_machines': JiraAttachmentForMachinesResource(client),
        'attachment_meta': JiraAttachmentMetaResource(client),
        'attachment_thumbnail': JiraAttachmentThumbnailResource(client),
        'audit_records': JiraAuditRecordsResource(client),
        'auto_complete': JiraAutoCompleteResource(client),
        'auto_complete_post': JiraAutoCompletePostResource(client),
        'available_screen_fields': JiraAvailableScreenFieldsResource(client),
        'available_time_tracking_implementations': JiraAvailableTimeTrackingImplementationsResource(client),
        'avatar': JiraAvatarResource(client),
        'avatar_image_by_id': JiraAvatarImageByIdResource(client),
        'avatar_image_by_owner': JiraAvatarImageByOwnerResource(client),
        'avatar_image_by_type': JiraAvatarImageByTypeResource(client),
        'avatars': JiraAvatarsResource(client),
        'banner': JiraBannerResource(client),
        'bulk_delete_issue': JiraBulkDeleteIssueResource(client),
        'bulk_get': JiraBulkGetResource(client),
        'bulk_get_users': JiraBulkGetUsersResource(client),
        'bulk_permissions': JiraBulkPermissionsResource(client),
        'bulk_set_issue': JiraBulkSetIssueResource(client),
        'bulk_set_issue_properties_by': JiraBulkSetIssuePropertiesByResource(client),
        'bulk_set_issues_properties': JiraBulkSetIssuesPropertiesResource(client),
        'cancel': JiraCancelResource(client),
        'change_filter': JiraChangeFilterResource(client),
        'change_logs': JiraChangeLogsResource(client),
        'change_logs_by_ids': JiraChangeLogsByIdsResource(client),
        'columns': JiraColumnsResource(client),
        'comment': JiraCommentResource(client),
        'comment_property': JiraCommentPropertyResource(client),
        'comment_property_keys': JiraCommentPropertyKeysResource(client),
        'comments': JiraCommentsResource(client),
        'comments_by_ids': JiraCommentsByIdsResource(client),
        'component': JiraComponentResource(client),
        'component_related_issues': JiraComponentRelatedIssuesResource(client),
        'configuration': JiraConfigurationResource(client),
        'contexts_for_field': JiraContextsForFieldResource(client),
        'contexts_for_field_deprecated': JiraContextsForFieldDeprecatedResource(client),
        'create_issue_meta': JiraCreateIssueMetaResource(client),
        'current_user': JiraCurrentUserResource(client),
        'custom_field': JiraCustomFieldResource(client),
        'custom_field_configuration': JiraCustomFieldConfigurationResource(client),
        'custom_field_context': JiraCustomFieldContextResource(client),
        'custom_field_context_from_projects': JiraCustomFieldContextFromProjectsResource(client),
        'custom_field_contexts_for_projects_and_issue_types': JiraCustomFieldContextsForProjectsAndIssueTypesResource(client),
        'custom_field_option': JiraCustomFieldOptionResource(client),
        'custom_field_value': JiraCustomFieldValueResource(client),
        'dashboard': JiraDashboardResource(client),
        'dashboard_item_property': JiraDashboardItemPropertyResource(client),
        'dashboard_item_property_keys': JiraDashboardItemPropertyKeysResource(client),
        'dashboards_paginated': JiraDashboardsPaginatedResource(client),
        'default_priority': JiraDefaultPriorityResource(client),
        'default_resolution': JiraDefaultResolutionResource(client),
        'default_screen_scheme': JiraDefaultScreenSchemeResource(client),
        'default_share_scope': JiraDefaultShareScopeResource(client),
        'default_values': JiraDefaultValuesResource(client),
        'default_workflow': JiraDefaultWorkflowResource(client),
        'do': JiraDoResource(client),
        'draft_default_workflow': JiraDraftDefaultWorkflowResource(client),
        'draft_workflow': JiraDraftWorkflowResource(client),
        'draft_workflow_mapping': JiraDraftWorkflowMappingResource(client),
        'dynamic_modules_resource': JiraDynamicModulesResourceResource(client),
        'dynamic_webhooks_for_app': JiraDynamicWebhooksForAppResource(client),
        'edit': JiraEditResource(client),
        'edit_issue_meta': JiraEditIssueMetaResource(client),
        'evaluate_jira': JiraEvaluateJiraResource(client),
        'events': JiraEventsResource(client),
        'failed_webhooks': JiraFailedWebhooksResource(client),
        'favourite_filters': JiraFavouriteFiltersResource(client),
        'favourite_for_filter': JiraFavouriteForFilterResource(client),
        'features_for_project': JiraFeaturesForProjectResource(client),
        'field_auto_complete_for_query_string': JiraFieldAutoCompleteForQueryStringResource(client),
        'field_configuration': JiraFieldConfigurationResource(client),
        'field_configuration_items': JiraFieldConfigurationItemsResource(client),
        'field_configuration_scheme': JiraFieldConfigurationSchemeResource(client),
        'field_configuration_scheme_mapping': JiraFieldConfigurationSchemeMappingResource(client),
        'field_configuration_scheme_mappings': JiraFieldConfigurationSchemeMappingsResource(client),
        'field_configuration_scheme_project_mapping': JiraFieldConfigurationSchemeProjectMappingResource(client),
        'field_to_default_screen': JiraFieldToDefaultScreenResource(client),
        'fields': JiraFieldsResource(client),
        'fields_paginated': JiraFieldsPaginatedResource(client),
        'filter': JiraFilterResource(client),
        'filters': JiraFiltersResource(client),
        'filters_paginated': JiraFiltersPaginatedResource(client),
        'find': JiraFindResource(client),
        'find_assignable': JiraFindAssignableResource(client),
        'find_bulk_assignable': JiraFindBulkAssignableResource(client),
        'find_user_keys_by': JiraFindUserKeysByResource(client),
        'find_users_and': JiraFindUsersAndResource(client),
        'find_users_by': JiraFindUsersByResource(client),
        'find_users_for': JiraFindUsersForResource(client),
        'find_users_with_all': JiraFindUsersWithAllResource(client),
        'find_users_with_browse': JiraFindUsersWithBrowseResource(client),
        'for_issues_using_jql': JiraForIssuesUsingJqlResource(client),
        'for_issues_using_jql_post': JiraForIssuesUsingJqlPostResource(client),
        'fully_update_project': JiraFullyUpdateProjectResource(client),
        'gadget': JiraGadgetResource(client),
        'group': JiraGroupResource(client),
        'hierarchy': JiraHierarchyResource(client),
        'ids_of_worklogs_deleted_since': JiraIdsOfWorklogsDeletedSinceResource(client),
        'ids_of_worklogs_modified_since': JiraIdsOfWorklogsModifiedSinceResource(client),
        'inactive_workflow': JiraInactiveWorkflowResource(client),
        'is_watching_issue_bulk': JiraIsWatchingIssueBulkResource(client),
        'issue': JiraIssueResource(client),
        'issue_all_types': JiraIssueAllTypesResource(client),
        'issue_field_option': JiraIssueFieldOptionResource(client),
        'issue_link': JiraIssueLinkResource(client),
        'issue_link_type': JiraIssueLinkTypeResource(client),
        'issue_link_types': JiraIssueLinkTypesResource(client),
        'issue_navigator_default_columns': JiraIssueNavigatorDefaultColumnsResource(client),
        'issue_picker_resource': JiraIssuePickerResourceResource(client),
        'issue_property': JiraIssuePropertyResource(client),
        'issue_property_keys': JiraIssuePropertyKeysResource(client),
        'issue_security_level': JiraIssueSecurityLevelResource(client),
        'issue_security_level_members': JiraIssueSecurityLevelMembersResource(client),
        'issue_security_scheme': JiraIssueSecuritySchemeResource(client),
        'issue_security_schemes': JiraIssueSecuritySchemesResource(client),
        'issue_type': JiraIssueTypeResource(client),
        'issue_type_avatar': JiraIssueTypeAvatarResource(client),
        'issue_type_from_issue_type_scheme': JiraIssueTypeFromIssueTypeSchemeResource(client),
        'issue_type_mappings_for_contexts': JiraIssueTypeMappingsForContextsResource(client),
        'issue_type_property': JiraIssueTypePropertyResource(client),
        'issue_type_property_keys': JiraIssueTypePropertyKeysResource(client),
        'issue_type_scheme': JiraIssueTypeSchemeResource(client),
        'issue_type_scheme_for_projects': JiraIssueTypeSchemeForProjectsResource(client),
        'issue_type_schemes_mapping': JiraIssueTypeSchemesMappingResource(client),
        'issue_type_screen_scheme': JiraIssueTypeScreenSchemeResource(client),
        'issue_type_screen_scheme_mappings': JiraIssueTypeScreenSchemeMappingsResource(client),
        'issue_type_screen_scheme_project_associations': JiraIssueTypeScreenSchemeProjectAssociationsResource(client),
        'issue_type_screen_schemes': JiraIssueTypeScreenSchemesResource(client),
        'issue_types_for_project': JiraIssueTypesForProjectResource(client),
        'issue_types_from_context': JiraIssueTypesFromContextResource(client),
        'issue_types_from_global_field_configuration_scheme': JiraIssueTypesFromGlobalFieldConfigurationSchemeResource(client),
        'issue_types_to_context': JiraIssueTypesToContextResource(client),
        'issue_types_to_issue_type_scheme': JiraIssueTypesToIssueTypeSchemeResource(client),
        'issue_watchers': JiraIssueWatchersResource(client),
        'issue_worklog': JiraIssueWorklogResource(client),
        'issues': JiraIssuesResource(client),
        'license': JiraLicenseResource(client),
        'link': JiraLinkResource(client),
        'locale': JiraLocaleResource(client),
        'mappings_for_issue_type_screen_scheme': JiraMappingsForIssueTypeScreenSchemeResource(client),
        'mappings_from_issue_type_screen_scheme': JiraMappingsFromIssueTypeScreenSchemeResource(client),
        'match': JiraMatchResource(client),
        'merge': JiraMergeResource(client),
        'migrate': JiraMigrateResource(client),
        'migration_resource': JiraMigrationResourceResource(client),
        'multiple_custom_field_values': JiraMultipleCustomFieldValuesResource(client),
        'my_filters': JiraMyFiltersResource(client),
        'my_permissions': JiraMyPermissionsResource(client),
        'notification_from_notification_scheme': JiraNotificationFromNotificationSchemeResource(client),
        'notification_scheme': JiraNotificationSchemeResource(client),
        'notification_scheme_for_project': JiraNotificationSchemeForProjectResource(client),
        'notification_scheme_to_project_mappings': JiraNotificationSchemeToProjectMappingsResource(client),
        'notification_schemes': JiraNotificationSchemesResource(client),
        'notifications': JiraNotificationsResource(client),
        'options_for_context': JiraOptionsForContextResource(client),
        'or_update_remote_issue_link': JiraOrUpdateRemoteIssueLinkResource(client),
        'parse_jql': JiraParseJqlResource(client),
        'partial_update_project': JiraPartialUpdateProjectResource(client),
        'permission_grant': JiraPermissionGrantResource(client),
        'permission_scheme': JiraPermissionSchemeResource(client),
        'permission_scheme_entity': JiraPermissionSchemeEntityResource(client),
        'permission_scheme_grant': JiraPermissionSchemeGrantResource(client),
        'permission_scheme_grants': JiraPermissionSchemeGrantsResource(client),
        'permitted_projects': JiraPermittedProjectsResource(client),
        'precomputations': JiraPrecomputationsResource(client),
        'preference': JiraPreferenceResource(client),
        'priorities': JiraPrioritiesResource(client),
        'priority': JiraPriorityResource(client),
        'project': JiraProjectResource(client),
        'project_asynchronously': JiraProjectAsynchronouslyResource(client),
        'project_avatar': JiraProjectAvatarResource(client),
        'project_category': JiraProjectCategoryResource(client),
        'project_category_by_id': JiraProjectCategoryByIdResource(client),
        'project_components': JiraProjectComponentsResource(client),
        'project_components_paginated': JiraProjectComponentsPaginatedResource(client),
        'project_context_mapping': JiraProjectContextMappingResource(client),
        'project_email': JiraProjectEmailResource(client),
        'project_issue_security_scheme': JiraProjectIssueSecuritySchemeResource(client),
        'project_property': JiraProjectPropertyResource(client),
        'project_property_keys': JiraProjectPropertyKeysResource(client),
        'project_role': JiraProjectRoleResource(client),
        'project_role_actors_for_role': JiraProjectRoleActorsForRoleResource(client),
        'project_role_actors_from_role': JiraProjectRoleActorsFromRoleResource(client),
        'project_role_actors_to_role': JiraProjectRoleActorsToRoleResource(client),
        'project_role_by_id': JiraProjectRoleByIdResource(client),
        'project_role_details': JiraProjectRoleDetailsResource(client),
        'project_roles': JiraProjectRolesResource(client),
        'project_type': JiraProjectTypeResource(client),
        'project_type_by_key': JiraProjectTypeByKeyResource(client),
        'project_versions': JiraProjectVersionsResource(client),
        'project_versions_paginated': JiraProjectVersionsPaginatedResource(client),
        'projects': JiraProjectsResource(client),
        'projects_for_issue_type_screen_scheme': JiraProjectsForIssueTypeScreenSchemeResource(client),
        'publish_draft_workflow': JiraPublishDraftWorkflowResource(client),
        'recent': JiraRecentResource(client),
        'refresh': JiraRefreshResource(client),
        'register_dynamic': JiraRegisterDynamicResource(client),
        'remote_issue_link': JiraRemoteIssueLinkResource(client),
        'remote_issue_link_by_global_id': JiraRemoteIssueLinkByGlobalIdResource(client),
        'remote_issue_link_by_id': JiraRemoteIssueLinkByIdResource(client),
        'remote_issue_links': JiraRemoteIssueLinksResource(client),
        'reorder_custom_field': JiraReorderCustomFieldResource(client),
        'reorder_issue_types_in_issue_type': JiraReorderIssueTypesInIssueTypeResource(client),
        'replace_issue_field': JiraReplaceIssueFieldResource(client),
        'reset': JiraResetResource(client),
        'reset_user': JiraResetUserResource(client),
        'resolution': JiraResolutionResource(client),
        'resolutions': JiraResolutionsResource(client),
        'root': JiraRootResource(client),
        'sanitise_jql': JiraSanitiseJqlResource(client),
        'screen': JiraScreenResource(client),
        'screen_scheme': JiraScreenSchemeResource(client),
        'screen_schemes': JiraScreenSchemesResource(client),
        'screen_tab': JiraScreenTabResource(client),
        'screen_tab_field': JiraScreenTabFieldResource(client),
        'screens': JiraScreensResource(client),
        'screens_for_field': JiraScreensForFieldResource(client),
        'security_levels_for_project': JiraSecurityLevelsForProjectResource(client),
        'select_time_tracking': JiraSelectTimeTrackingResource(client),
        'selectable_issue_field_options': JiraSelectableIssueFieldOptionsResource(client),
        'selected_time_tracking_implementation': JiraSelectedTimeTrackingImplementationResource(client),
        'server_info': JiraServerInfoResource(client),
        'share_permission': JiraSharePermissionResource(client),
        'share_permissions': JiraSharePermissionsResource(client),
        'shared_time_tracking_configuration': JiraSharedTimeTrackingConfigurationResource(client),
        'status': JiraStatusResource(client),
        'status_categories': JiraStatusCategoriesResource(client),
        'status_category': JiraStatusCategoryResource(client),
        'statuses': JiraStatusesResource(client),
        'statuses_by_id': JiraStatusesByIdResource(client),
        'store': JiraStoreResource(client),
        'task': JiraTaskResource(client),
        'toggle_feature_for': JiraToggleFeatureForResource(client),
        'transitions': JiraTransitionsResource(client),
        'trashed_fields_paginated': JiraTrashedFieldsPaginatedResource(client),
        'ui_modification': JiraUiModificationResource(client),
        'ui_modifications': JiraUiModificationsResource(client),
        'user': JiraUserResource(client),
        'user_columns': JiraUserColumnsResource(client),
        'user_default_columns': JiraUserDefaultColumnsResource(client),
        'user_email': JiraUserEmailResource(client),
        'user_email_bulk': JiraUserEmailBulkResource(client),
        'user_from_group': JiraUserFromGroupResource(client),
        'user_groups': JiraUserGroupsResource(client),
        'user_property': JiraUserPropertyResource(client),
        'user_property_keys': JiraUserPropertyKeysResource(client),
        'user_to_group': JiraUserToGroupResource(client),
        'users_from_group': JiraUsersFromGroupResource(client),
        'valid_project_key': JiraValidProjectKeyResource(client),
        'valid_project_name': JiraValidProjectNameResource(client),
        'validate_project': JiraValidateProjectResource(client),
        'version': JiraVersionResource(client),
        'version_related_issues': JiraVersionRelatedIssuesResource(client),
        'version_unresolved_issues': JiraVersionUnresolvedIssuesResource(client),
        'visible_issue_field_options': JiraVisibleIssueFieldOptionsResource(client),
        'vote': JiraVoteResource(client),
        'votes': JiraVotesResource(client),
        'watcher': JiraWatcherResource(client),
        'webhook_by_id': JiraWebhookByIdResource(client),
        'workflow': JiraWorkflowResource(client),
        'workflow_mapping': JiraWorkflowMappingResource(client),
        'workflow_scheme': JiraWorkflowSchemeResource(client),
        'workflow_scheme_draft': JiraWorkflowSchemeDraftResource(client),
        'workflow_scheme_draft_from_parent': JiraWorkflowSchemeDraftFromParentResource(client),
        'workflow_scheme_draft_issue_type': JiraWorkflowSchemeDraftIssueTypeResource(client),
        'workflow_scheme_issue_type': JiraWorkflowSchemeIssueTypeResource(client),
        'workflow_scheme_project_associations': JiraWorkflowSchemeProjectAssociationsResource(client),
        'workflow_transition_properties': JiraWorkflowTransitionPropertiesResource(client),
        'workflow_transition_property': JiraWorkflowTransitionPropertyResource(client),
        'workflow_transition_rule_configurations': JiraWorkflowTransitionRuleConfigurationsResource(client),
        'workflows_paginated': JiraWorkflowsPaginatedResource(client),
        'worklog': JiraWorklogResource(client),
        'worklog_property': JiraWorklogPropertyResource(client),
        'worklog_property_keys': JiraWorklogPropertyKeysResource(client),
        'worklogs_for_ids': JiraWorklogsForIdsResource(client),
    }
