<script setup lang="ts">
import { TaskType } from '@/types/task-type';
import { useTaskStore } from '@/store/tasks';
import { useBalancesBreakdown } from '@/composables/balances/breakdown';
import AssetBalances from '@/components/AssetBalances.vue';
import type { AssetBalanceWithPrice } from '@rotki/common';

const props = defineProps<{
  identifier: string;
}>();

const { identifier } = toRefs(props);
const { isTaskRunning } = useTaskStore();

const { t } = useI18n();

const { locationBreakdown: breakdown } = useBalancesBreakdown();
const locationBreakdown: ComputedRef<AssetBalanceWithPrice[]> = breakdown(identifier);

const loadingData = computed<boolean>(
  () =>
    get(isTaskRunning(TaskType.QUERY_BLOCKCHAIN_BALANCES))
    || get(isTaskRunning(TaskType.QUERY_EXCHANGE_BALANCES))
    || get(isTaskRunning(TaskType.QUERY_BALANCES)),
);
</script>

<template>
  <RuiCard v-if="loadingData || locationBreakdown.length > 0">
    <template #header>
      {{ t('common.assets') }}
    </template>
    <AssetBalances
      :loading="loadingData"
      :balances="locationBreakdown"
      hide-breakdown
      sticky-header
    />
  </RuiCard>
</template>
