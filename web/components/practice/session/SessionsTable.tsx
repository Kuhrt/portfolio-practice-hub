'use client';

import {
  ColumnDef,
  getCoreRowModel,
  useReactTable
} from '@tanstack/react-table';

import { DataTable } from '@/components/ui/data-table/data-table';
import { DataTablePagination } from '@/components/ui/data-table/data-table-pagination';
import { PracticeSession, SessionTypeLabel } from '@/models/practice';
import { formatDateTime, formatTime } from '@/utils/dates';

interface Props {
  sessions: PracticeSession[];
}

export default function SessionsTable({ sessions }: Props) {
  const columns: ColumnDef<PracticeSession>[] = [
    {
      header: 'Type',
      accessorKey: 'session_type',
      cell: ({ row }) => {
        return <span>{SessionTypeLabel.get(row.original.session_type)}</span>;
      }
    },
    {
      header: 'Description',
      accessorKey: 'description',
      cell: ({ row }) => {
        return row.original.description || '-';
      }
    },
    {
      header: 'Time Spent',
      accessorKey: 'duration',
      cell: ({ row }) => {
        const duration =
          row.original.duration > 0 ? formatTime(row.original.duration) : '';
        const startTime = formatDateTime(row.original.started_at);
        const endTime = !!row.original.stopped_at
          ? ` - ${formatDateTime(row.original.stopped_at)}`
          : '';
        return (
          <span>
            {duration} ({startTime}
            {endTime})
          </span>
        );
      }
    }
  ];

  const table = useReactTable({
    data: sessions,
    columns,
    getCoreRowModel: getCoreRowModel()
  });

  return (
    <>
      <DataTable table={table} />
      <DataTablePagination table={table} />
    </>
  );
}
